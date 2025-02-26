from google import genai
from dotenv import load_dotenv
import os
import PyPDF2

# Load environment variables
load_dotenv()

# Configure the API
api_key = os.getenv("API_KEY")

# Function to extract text from PDF
def pdf_to_text(file_path):
    try:
        text = ""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                text += reader.pages[page_num].extract_text()
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

# Extract text from the PDF file
pdf_path = "Apology.pdf"
pdf_content = pdf_to_text(pdf_path)

if pdf_content:
    # Initialize the model
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    # Generate flashcards from the PDF content
    response = model.generate_content(
        "Create flashcards in question and answer format based on the following content from 'Apology' by Plato:\n\n" + pdf_content
    )
    
    # Print the generated flashcards
    print(response.text)
else:
    print("Failed to extract text from the PDF file.")



