from google import genai
from dotenv import load_dotenv
import os
import PyPDF2
import json

# Load environment variables
load_dotenv()

# Configure the API
client = genai.Client(api_key=os.getenv("API_KEY"))


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
        print(f"Error reading PDF: {e}")
        return None


# Extract text from the PDF file
pdf_path = "/Users/alexgallardo/Downloads/Phaedo.pdf"
pdf_content = pdf_to_text(pdf_path)

prompt = (
    f" Create flashcards in question and answer format based on the following content {pdf_content}"
    """Use this JSON schema:

Flashcards = {'question': str, 'answer': str}
Return: list[Flashcards]"""
)


if pdf_content:
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    # Print the generated flashcards
    if response.text.startswith("```json"):
        text = response.text[7:]
    else:
        text = response.text
    if text.endswith("```"):
        text = text[:-3]
        flashcards_dict = json.loads(text)
        print(flashcards_dict)
else:
    print("Failed to extract text from the PDF file.")
