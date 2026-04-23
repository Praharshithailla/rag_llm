import requests
from prompt import build_prompt

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:latest"


def chat_with_model(context: str, question: str, history: str):

    # Build prompt with context + history
    full_prompt = build_prompt(context, question, history)

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": full_prompt,
            "stream": False,
            "temperature": 0.2
        }
    )

    if response.status_code == 200:
        return response.json()["response"].strip()
    else:
        return f"Error: {response.status_code}"