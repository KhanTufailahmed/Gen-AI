from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from pathlib import Path
from langchain_qdrant import QdrantVectorStore

load_dotenv()
pdf_path = Path(__file__).parent / "nodejs.pdf"

loader = PyPDFLoader(file_path=pdf_path)

doc = loader.load()

# print("\n", doc[0])  # Read PDF File

# Now we have to do chunking of the pdf

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=400,
)


split_docs=text_splitter.split_documents(documents=doc)

# Next we have to do the vector enbedding 

embedding_model=OpenAIEmbeddings(
    model="text-embedding-3-small"
)

# now we have have created the embedding model up next we will create the embedding and store it in qdrant db
vector_store=QdrantVectorStore.from_documents(
    documents=split_docs,
    url="http://localhost:6333",
    collection_name="NodejsRAG",
    embedding=embedding_model,
)#done with the indexing of the doc

