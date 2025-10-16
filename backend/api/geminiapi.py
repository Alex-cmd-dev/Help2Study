from google import genai
from django.conf import settings
from dotenv import load_dotenv
import os
import json
import logging
from .models import Flashcard
from .utils.text_extractors import extract_text_from_file


load_dotenv()
logger = logging.getLogger(__name__)

# Configure the API with error handling
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError(
        "API_KEY not found in environment variables. "
        "Please create a .env file with your Gemini API key. "
        "See .env.example for reference."
    )
client = genai.Client(api_key=api_key)


# Maximum file size: 10MB
MAX_FILE_SIZE = 10 * 1024 * 1024


# Function to process uploaded file and save it temporarily
def processfile(uploaded_file):
    # Validate file size
    if uploaded_file.size > MAX_FILE_SIZE:
        raise ValueError(
            f"File too large. Maximum size is {MAX_FILE_SIZE / (1024 * 1024):.0f}MB. "
            f"Your file is {uploaded_file.size / (1024 * 1024):.1f}MB."
        )

    temp_dir = os.path.join(settings.BASE_DIR, "temp_files")
    os.makedirs(temp_dir, exist_ok=True)  # Ensure directory exists
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb+") as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    return file_path


# Text extraction functions moved to utils/text_extractors.py
# This keeps the code organized and reusable!


# Function to generate flashcards from text
def text_2flashcards(text):
    try:
        logger.info(f"Input text for flashcards: {text}")  # logs text from file
        prompt = (
            f"Create flashcards in JSON format based on the following content: {text}\n"
            "Format strictly as a JSON array of objects with 'question' and 'answer' keys.\n"
            "Example: [{'question': 'What is...?', 'answer': 'This is...'}, ...]\n"
            "Ensure valid JSON formatting."
        )
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash", contents=prompt
            )
        except Exception as api_error:
            logger.error(f"API call failed: {api_error}")
            raise ValueError(f"Gemini API call failed: {api_error}")

        logger.info(f"Raw response: {response.text}")  # log response from api

        if response.text.startswith("```json"):
            text = response.text[7:]
        else:
            text = response.text
        if text.endswith("```"):
            text = text[:-3]
        flashcards_dict = json.loads(text)

        return flashcards_dict
    except Exception as e:
        raise ValueError(f"Failed to generate flashcards: {str(e)}")


# Main function to create flashcards from files
def create_flashcards(file_path, mime_type):
    try:
        # Extract text using our utility function
        # (Text extraction logic is now in utils/text_extractors.py)
        text = extract_text_from_file(file_path, mime_type)

        # Generate flashcards from extracted text
        flashcards = text_2flashcards(text)

        return flashcards

    except Exception as e:
        raise ValueError(f"Something went wrong: {str(e)}")


def handle_flashcard_creation(uploaded_file, topic, user):
    mime_type = uploaded_file.content_type

    try:
        file_path = processfile(uploaded_file)
        flashcards = create_flashcards(file_path, mime_type)

        created_flashcards = []
        for flashcard in flashcards:
            fcard = Flashcard.objects.create(
                user=user,
                topic=topic,
                question=flashcard["question"],
                answer=flashcard["answer"],
            )
            created_flashcards.append(fcard)

        if file_path and os.path.exists(file_path):
            os.remove(file_path)

    except Exception as e:
        # Clean up the temporary file in case of errors
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        raise Exception(f"Processing failed: {str(e)}")
