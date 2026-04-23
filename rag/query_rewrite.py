def rewrite_query(user_query,chat_history):
    if len(chat_history) == 0:
        return user_query
    last_question = chat_history[-1]["user"]
    rewritten_query = f"{last_question} {user_query}"
    return rewritten_query
