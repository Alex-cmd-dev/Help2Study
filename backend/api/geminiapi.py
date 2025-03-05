from google import genai
import docx2txt
from django.conf import settings
from dotenv import load_dotenv
import os
import PyPDF2
import json
import logging
from .models import Flashcard
from .serializers import FlashcardSerializer


load_dotenv()
logger = logging.getLogger(__name__)

# Configure the API
client = genai.Client(api_key=os.getenv("API_KEY"))


# Function to process uploaded file and save it temporarily
def processfile(uploaded_file):
    temp_dir = os.path.join(settings.BASE_DIR, "temp_files")
    os.makedirs(temp_dir, exist_ok=True)  # Ensure directory exists
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb+") as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    return file_path


# Function to extract text from PDF
def pdf_to_text(file_path):
    try:
        text = ""
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                text += reader.pages[page_num].extract_text()
        return text
    except Exception as e:
        raise ValueError(f"Failed to read PDF file: {str(e)}")


# Function to extract text from DOCX
def docx_to_text(file_path):
    try:
        text = docx2txt.process(file_path)
        return text
    except Exception as e:
        raise ValueError(f"Failed to read docx file: {str(e)}")


# Function to extract text from TXT
def read_text_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        raise ValueError(f"Failed to read text file: {str(e)}")


# Function to generate flashcards from text
def text_2flashcards(text):
    try:
        logger.info(f"Input text for flashcards: {text}") #logs text from file
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
        
        logger.info(f"Raw response: {response.text}") #log response from api

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
        # Extract text based on file type
        if mime_type == "application/pdf":
            text = pdf_to_text(file_path)
        elif mime_type == "text/plain":
            text = read_text_file(file_path)
        elif (
            mime_type
            == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ):
            text = docx_to_text(file_path)
        else:
            raise Exception(f"Unsupported file type: {mime_type}")

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
        serializer = FlashcardSerializer(created_flashcards, many=True)

    except Exception as e:
        # Clean up the temporary file in case of errors
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        raise Exception(f"Processing failed: {str(e)}")
