from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key=os.getenv("API_KEY"))

uploaded_file = genai.upload_file(
    path="Apology.pdf",
    display_name="uploaded_file",
    mime_type="application/pdf",
)


model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[
        "Create Flashcards in questions and answer format",
        uploaded_file,
    ],
)


print(response)
