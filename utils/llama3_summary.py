import os
from groq import Groq
def generate_summary(text):
    client = Groq(
        api_key="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",
    )
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Summarize this text in 100 words: {text}",
            }
        ],
        model="llama-3.1-8b-instant",
    )
    print(chat_completion.choices[0].message.content)
    return chat_completion.choices[0].message.content