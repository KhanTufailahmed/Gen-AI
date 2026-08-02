from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT = """
    You are an AI Expert in Coding. You Only know Python and nothig else.
    You help users in solving there Python doubts only and nothing else.
    If user tried to ask something else apart from Python you can roast them.
"""

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Hey,My Name is Tufail Ahmed"},
        {"role":"assistant","content":"Hey Piyush! How can I help you with Python coding today?"},
        {"role":"user","content":"Hey i just wanted to ask how to write a sum function in Java"},
    ],
)

print(response.choices[0].message.content)
