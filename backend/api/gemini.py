from google import genai
from dotenv import load_dotenv
import os

load_dotenv()


sys_instruct = "You are a cat. Your name is Neko."
client = genai.Client(api_key="GEMINI_API_KEY")

def gemini(text):
    response = client.models.generate_content(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(system_instruction=sys_instruct),
    contents=["your prompt here"],
)
