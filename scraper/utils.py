import pinecone      
import openai
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup


load_dotenv("../.env")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

def createPineconeInstance():
    pinecone.init(      
        api_key='8933a9da-5c77-4209-b89b-8884efef24be',  #leaving this in here cuz we have to connect to the same index    
        environment='us-east1-gcp'      
    )
    index = pinecone.Index('readerproject')
    return index
def extract_text(html, clean=True):
    soup = BeautifulSoup(html, 'html.parser')
    # Using .get_text() method to extract all the text 
    text = soup.get_text()
    if clean:
        text.replace("\n", " ")
    return text
def chunk(text):
    chunks = text.split(".")
    return chunks
def embed(chunks, model = "text-embedding-ada-002", pineconeIndex=None):
    newPineconeIndex = pineconeIndex
    if pineconeIndex == None:
        newPineconeIndex = createPineconeInstance()
    res = openai.Embedding.create(
        input=chunks,
        engine=model
    )
    embeds = [rec['embedding'] for rec in res['data']]
    metadata = [{"text": chunk} for chunk in chunks]
    to_include = zip(embeds, metadata)
    newPineconeIndex.upsert(vectors = list(to_include))





