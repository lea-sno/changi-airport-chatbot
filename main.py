import os
import requests
from bs4 import BeautifulSoup
import openai
from langchain.chains import RetrievalQA
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

#  Scrape and Clean Website Content
def scrape_and_clean(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch URL {url}: {response.status_code}")

    soup = BeautifulSoup(response.content, "html.parser")
    # Extract relevant text, e.g., paragraphs and headings
    text = ' '.join([tag.get_text(strip=True) for tag in soup.find_all(['p', 'h1', 'h2', 'h3'])])
    return text

# Scrape Changi Airport and Jewel Changi Airport content
changi_url = "https://www.changiairport.com"
jewel_url = "https://www.jewelchangiairport.com"

changi_content = scrape_and_clean(changi_url)
jewel_content = scrape_and_clean(jewel_url)

# Step 2: Vectorize Data and Store in a Vector Database
openai.api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_environment = os.getenv("PINECONE_ENV")

# Initialize Pinecone
pinecone.init(api_key=pinecone_api_key, environment=pinecone_environment)
index_name = "changi-airport"

# Ensure the index exists
if index_name not in pinecone.list_indexes():
    pinecone.create_index(index_name, dimension=1536)

db = Pinecone.from_existing_index(
    index_name=index_name, 
    embedding_function=OpenAIEmbeddings()
)

# Embed and store website content
texts = [changi_content, jewel_content]
metadata = [{"source": changi_url}, {"source": jewel_url}]
db.add_texts(texts=texts, metadatas=metadata)

# Step 3: Develop the Chatbot
class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str

# Initialize LangChain Retrieval QA chain
retriever = db.as_retriever()
qa_chain = RetrievalQA.from_chain_type(
    llm=openai.ChatCompletion(),
    retriever=retriever,
    return_source_documents=True
)

# Step 4: Deploy with FastAPI
app = FastAPI()

@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    try:
        result = qa_chain.run(request.query)
        return QueryResponse(answer=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# API Documentation
@app.get("/")
def root():
    return {"message": "Welcome to the Changi Airport Chatbot API! Use /query to ask questions."}

# Run the FastAPI app (for local testing)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
