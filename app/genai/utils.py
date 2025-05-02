import os
import httpx
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def generate_summary(feedbacks: list[str]) -> str:
    if not GROQ_API_KEY:
        return "Error: Groq API key is missing."

    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}

    prompt = "Summarize the following feedbacks from tasks assigned to a user:\n" + "\n".join(feedbacks)

    payload = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]}   # llama3-8b-8192


    try:
        response = httpx.post(GROQ_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response")

    except httpx.HTTPStatusError as e:
        return f"API Error: {e.response.status_code}"
    except Exception as e:
        return f"Unexpected Error: {str(e)}"
