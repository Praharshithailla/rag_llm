def build_prompt(context: str, question: str, history: str) -> str:

    return f"""
You are an AI tutor for CS students.

Conversation History:
{history}

Use the following context to answer the question.

Context:
{context}

Answer strictly in this format:

Definition:
Explanation:
Example:
Advantages:
Disadvantages:
Source:

Question: {question}
"""