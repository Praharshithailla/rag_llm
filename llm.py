import os
from prompt import build_prompt
from openai import OpenAI

# Initialize client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_with_model(context: str, question: str, history: str):
    try:
        # Debug: check API key loaded or not
        print("API KEY LOADED:", os.getenv("OPENAI_API_KEY"))

        # Build prompt
        full_prompt = build_prompt(context, question, history)

        # Debug: prompt check (optional)
        print("PROMPT:", full_prompt[:200])  # first 200 chars

        # OpenAI call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.2
        )

        return response.choices[0].message.content

    except Exception as e:
        print("🔥 FULL ERROR:", e)   # terminal lo full error
        return f"ERROR: {str(e)}"    # UI lo kuda error chupisthundi