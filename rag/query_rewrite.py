def rewrite_query(user_query, chat_history):

    if len(chat_history) == 0:
        return user_query

    last_question = chat_history[-1]["user"]

    # Avoid duplication
    if user_query.lower() in last_question.lower():
        return user_query

    return f"{last_question}. {user_query}"