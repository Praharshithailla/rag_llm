import requests
from prompt import build_prompt

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.2"


def chat_with_model(context: str, question: str, history: str):
    try:
        # 🔧 Build prompt
        full_prompt = build_prompt(context, question, history)

        print("\n[DEBUG] Sending to Ollama (chat API)...")

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant."
                    },
                    {
                        "role": "user",
                        "content": full_prompt
                    }
                ],
                "stream": False,
                "options": {
                    "temperature": 0.2
                }
            },
            timeout=120
        )

        # ❌ Error handling
        if response.status_code != 200:
            print("❌ Ollama Error:", response.text)
            return f"Error: {response.status_code}"

        data = response.json()

        # ✅ NEW FORMAT
        answer = data.get("message", {}).get("content", "").strip()

        return answer if answer else "⚠️ Empty response"

    except requests.exceptions.Timeout:
        return "Model is slow. Please try again."

    except Exception as e:
        print("🔥 ERROR:", str(e))
        return f"ERROR: {str(e)}"