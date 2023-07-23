from utils import chunk, embed, extract_text, summarizeIt, getHTML
import sys
import modal
from modal import web_endpoint
from otherUtils import get_reasons
# import requests



# # get some html just to prove that this works
# r = requests.get("https://docs.pinecone.io/docs/openai")
# # print(r.text)
# print(embed(chunk(extract_text(r.text))))
reader_image = modal.Image.debian_slim().pip_install("openai", "beautifulsoup4", "pinecone-client", "langchain")


stub = modal.Stub("reader-project")


@stub.function(image=reader_image, secret=modal.Secret.from_name("my-openai-secret-2"))
@web_endpoint()
def pushtovec(link):
    embed(chunk(extract_text(getHTML(link))))
    return True

@stub.function(image=reader_image, secret=modal.Secret.from_name("my-openai-secret-2"))
@web_endpoint()
def summarize(link):

    summary = summarizeIt(extract_text(getHTML(link)))
    return get_reasons(summary)


