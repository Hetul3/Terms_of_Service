import os
from app.config import Config
from groq import Groq

groq_key = Config.GROQ_KEY

def query_llm(prompt, max_tokens=100, temperature=0.3):
    client = Groq(
        api_key=groq_key,
    )
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ], 
        model="llama3-8b-8192",
        max_tokens=max_tokens,
        temperature=temperature,
    )
    print(chat_completion.choices[0].message)
    return chat_completion.choices[0].message.content