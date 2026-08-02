from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI()

text="dog chases cat"

response=client.embeddings.create(
    input=text,
    model="text-embedding-3-small"
)

print(response.data[0].embedding)