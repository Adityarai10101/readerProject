from utils import chunk, embed, extract_text, summarizeIt
import sys
import modal
from modal import web_endpoint
# import requests



# # get some html just to prove that this works
# r = requests.get("https://docs.pinecone.io/docs/openai")
# # print(r.text)
# print(embed(chunk(extract_text(r.text))))
reader_image = modal.Image.debian_slim().pip_install("openai", "beautifulsoup4", "pinecone-client")


stub = modal.Stub("reader-project")


@stub.function(image=reader_image)
@web_endpoint()
def pushtovec(text):
    embed(chunk(extract_text(text)))
    return True

@stub.function(image=reader_image)
@web_endpoint()
def summarize(text):
    return summarizeIt(extract_text(text))

