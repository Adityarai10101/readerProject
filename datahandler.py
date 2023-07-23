import os
from dotenv import load_dotenv
load_dotenv()
from psychicapi import Psychic, ConnectorId
from langchain.schema import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.llms import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.document_loaders import PsychicLoader
from langchain.text_splitter import CharacterTextSplitter
import pinecone
# Initialize Psychic with secret key
# psychic = Psychic(secret_key=os.getenv("PSYCHIC_SECRET_KEY"))

# Get all active connections and optionally filter by connector id and/or account id
# raw_docs = psychic.get_documents(account_id='hackathon', chunked=True)

# Load documents from Notion using PsychicLoader

def load_user_data(connector_id):
    notion_loader = PsychicLoader(api_key="78ae72e3-aa7b-4f37-9f96-aa420094b0b1", account_id="bkitano-personal", connector_id=ConnectorId.notion.value)

    pinecone.init(api_key="b6a60048-29ac-4843-a441-a6bd0fdb7bc3", environment="asia-southeast1-gcp-free")
    docs = notion_loader.load()
    # print datatpye of docs
    print(docs)
    print(type(docs))
    embeddings = OpenAIEmbeddings()
    #docsearch = Pinecone.from_documents(docs, embeddings, index_name='hackothin')
    # Create a Pinecone vectorstore from the documents
    #vectorstore = Pinecone.from_documents(docs, embeddings)

    docsearch = Pinecone.from_documents(docs, embeddings, index_name='hackothin')



load_user_data("notion")

