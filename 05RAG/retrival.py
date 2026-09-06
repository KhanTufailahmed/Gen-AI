from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="NodejsRAG",
    embedding=embedding_model,
)


# Take user Query
query = input("Enter your query: \n\n")

# Vector similarity search in db of user query

search_result = vector_db.similarity_search(
    query=query,
)

# print("Search Result: \n", search_result)

context = "\n\n\n".join(
    [
        f"Page content: {result.page_content}\n Page number:{result.metadata['page_label']}\n File location:{result.metadata['source']}\n"
        for result in search_result
    ]
)


SYSTEM_PROMPT = f"""
    You are a helpfull AI assistant who is specialized in resolving user query based on the avaialable context retrieved from a PDF file along with page_contents and page number.
    
    You should only ans the user based on the following context and navigate the user to open the right page number to know more.
    
    Context: 
        {context}
"""



chat_completion = client.chat.completions.create(
    model='gpt-4.1',
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": query},
    ],
)
# print(SYSTEM_PROMPT)


print(f"🤖: {chat_completion.choices[0].message.content} ")