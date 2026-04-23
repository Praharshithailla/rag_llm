chat_history=[]

def add_message(user,assistant):
    chat_history.append({
        "user": user,
        "assistant": assistant
    })
def get_history():
    history_text = ""
    for chat in chat_history:
        history_text += f"User: {chat['user']}\n"
        history_text += f"Assistant: {chat['assistant']}\n\n"

    return history_text
