from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()


sys_instruct = "You are a college professor"
client = genai.Client(api_key=os.getenv("API_KEY"))


def gemini(text):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(system_instruction=sys_instruct),
            contents=[
                f"Create a detailed summary that allows understanding for tests,assignments, and discussions, this is the text,  {text}"
            ],
        )
        return response
    except Exception as e:
        raise ValueError(f"Failed to create summary: {e}")
