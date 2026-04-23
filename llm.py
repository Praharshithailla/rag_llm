import os
from prompt import build_prompt
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_with_model(context: str, question: str, history: str):

    full_prompt = build_prompt(context, question, history)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": full_prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content