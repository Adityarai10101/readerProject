import pinecone      
import openai
import os
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm


def createPineconeInstance():
    pinecone.init(      
        api_key='8933a9da-5c77-4209-b89b-8884efef24be',  #leaving this in here cuz we have to connect to the same index    
        environment='us-east1-gcp'      
    )
    
    
    # print(pinecone.describe_index("readerproject"))
    index = pinecone.Index('readerproject')
    numVecs = int(index.describe_index_stats()["namespaces"][""]["vector_count"])
    print("deleting")
    for i in tqdm(range(0, numVecs, 32)):
        endi = min(i+32, numVecs)
        vecsBatch = range(i, endi)
        idsBatch = [str(n) for n in vecsBatch]
        index.delete(ids=idsBatch)
    return index
def extract_text(html, clean=True):
    soup = BeautifulSoup(html, 'html.parser')
    # Using .get_text() method to extract all the text 
    text = soup.get_text()
    if clean:
        text = text.replace("\n", ".")
    return text
def chunk(text):
    chunks = text.split(".")
    filtered_chunks = [chunk for chunk in chunks if chunk != '']
    # print(filtered_chunks)
    return filtered_chunks
def embed(chunks, model = "text-embedding-ada-002", pineconeIndex=None, batch_size=32):    
    newPineconeIndex = pineconeIndex
    if pineconeIndex == None:
        newPineconeIndex = createPineconeInstance()
    res = openai.Embedding.create(
        input=chunks,
        engine=model
    )
    # print(res)
    # print(chunks)
    embeds = [rec['embedding'] for rec in res['data']]
    metadata = [{"text": chunk} for chunk in chunks]
    # print(len(embeds))
    print('adding')
    for i in tqdm(range(0, len(embeds), batch_size)):
        endi = min(i+batch_size, len(embeds))
        embedsBatch = embeds[i:endi]
        idsBatch = [str(n) for n in range(i, endi)]
        metaBatch = metadata[i:endi]
        to_include = zip(idsBatch, embedsBatch, metaBatch)
        # print(list(to_include))
        # print(to_include)
        # print(to_include)
        newPineconeIndex.upsert(vectors = list(to_include))  
    # to_include = zip(embeds, metadata)
    # newPineconeIndex.upsert(vectors = list(to_include))
    return True

def summarizeIt(text):
    # print(text)
    completion = openai.ChatCompletion.create(
    model="gpt-4-0613",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that specializes in summarizing text."},
        {"role": "user", "content": f"{text} \n Please summarize the above text:"}
    ]
    )
    return completion["choices"][0]["message"]["content"]

def getHTML(pageLink):
    response = requests.get(pageLink)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.prettify()
