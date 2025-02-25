from google import genai
from google.genai import types
import docx2txt
from django.conf import settings
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))


def create_flashcards(file_path):
    
    pass


def processfile(uploaded_file):
    temp_dir = os.path.join(settings.BASE_DIR, "temp_files")
    os.makedirs(temp_dir, exist_ok=True)  # Ensure directory exists
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb+") as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    return file_path


def toText(file_type, file):
    try:
        if (
            file_type
            == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ):
            return docx_to_text(file)
        else:
            raise Exception(f"Unsupported file type: {file_type}")
    except Exception as e:
        raise ValueError(f"Something went wrong: {str(e)}")


def docx_to_text(docx):
    try:
        text = docx2txt.process(f"{docx}")
        return text
    except Exception as e:
        raise ValueError(f"Failed to read docx file: {str(e)}")
