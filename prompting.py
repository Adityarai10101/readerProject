from pprint import pprint

#from openai_function_call import OpenAISchema
#from openai_function_call.dsl import ChatCompletion, MultiTask, messages as m
#from openai_function_call.dsl.messages import SystemIdentity, SystemTask, SystemStyle, SystemGuidelines, SystemTips
from langchain.embeddings.openai import OpenAIEmbeddings
import openai
import json
# Define a subtask you'd like to extract from then,
# We'll use MultTask to easily map it to a List[Search]
# so we can extract more than one
import pinecone
from langchain.vectorstores import Pinecone

def load_html_data(pinecone_index_name:str):

    pinecone.init(api_key="b6a60048-29ac-4843-a441-a6bd0fdb7bc3", environment="asia-southeast1-gcp-free")
 
    embeddings = OpenAIEmbeddings()
    

    docsearch = Pinecone.from_documents(docs, embeddings, index_name='hackothin')

def load_notion_data(query:str):
    embeddings = OpenAIEmbeddings()
    pinecone.init(api_key="b6a60048-29ac-4843-a441-a6bd0fdb7bc3", environment="asia-southeast1-gcp-free")
    index = pinecone.Index("hackothin")
    vectorstore = Pinecone(index, embeddings.embed_query, "source")
    top_docs = vectorstore.similarity_search(query, k=3)
    return top_docs
class Notion:
    content: str
    source: str
#function_call = 
#notion_example = [Document(page_content='https://www.notion.so/Getting-Started-214f146d408945139daca97560a5e56a', metadata={'text': "<div><h1>Getting Started</h1><p>👋 Welcome to Notion!</p><p></p><p>Here are the basics:</p><p></p><p>See it in action:</p><p></p><p></p><p></p><p>Visit our  <a href='http://youtube.com/c/notion'>YouTube channel</a>  to watch 50+ more tutorials</p><p></p><p>👉 Have a question?  Click the  ?  at the bottom right for more guides, or to send us a message.</p><p></p></div>", 'title': 'Getting Started'})]
notion_example_content = """page_content='https://www.notion.so/Getting-Started-214f146d408945139daca97560a5e56a', metadata={'text': "<div><h1>Getting Started</h1><p>👋 Welcome to Notion!</p><p></p><p>Here are the basics:</p><p></p><p>See it in action:</p><p></p><p></p><p></p><p>Visit our  <a href='http://youtube.com/c/notion'>YouTube channel</a>  to watch 50+ more tutorials</p><p></p><p>👉 Have a question?  Click the  ?  at the bottom right for more guides, or to send us a message.</p><p></p></div>"""
notion_exmaple_source = "https://www.notion.so/Getting-Started-214f146d408945139daca97560a5e56a"
html_summarization_example = """
This webpage provides comprehensive information about effective note taking strategies for students, professionals, and anyone interested in improving their note-taking skills. It is well-structured and user-friendly, allowing easy navigation through various topics.

"The Importance of Note Taking": This section covers the benefits of effective note-taking, such as improved comprehension, retention of information, and better preparation for exams or meetings.

"Types of Note Taking Methods": Here, the page details several note-taking techniques, including the Cornell Method, Outlining, Mapping, and the Charting Method. Each method is explained with examples and situations where they might be most useful.
"""
'''
tasks = (
    ChatCompletion(name="HTML Important information parsing", model="gpt-3.5-turbo-0613")
    | SystemIdentity(identity="World class state of the art agent") # if no identity is provided, this is the default one
    | SystemTask(task="Tell me the data on this page that is most relevant to me ")
    | SystemStyle(style="Professional, clear and concise")
    | SystemGuidelines(guidelines=[
        'You never swear',
        'You are polite',
        'You say please and thank you often.'
    ])
    | SystemTips(tips=[
        "When unsure about the correct information, try to think about the task as a whole",
        "If acronyms are used expand them to their full form",
        "Use multiple phrases to describe the same thing"]
                  )
    | MultiTask(subtask_class=Search)
    | m.TaggedMessage(
        tag="notion",
        content="Can you tell me how the following information is relevant to me?",
    )

    | 

    | m.ChainOfThought()
)
'''




output = []
functions = [{
    "name": "get_notion_relevance",
    "description": "Give a short one sentence summary about how the HTML is related to my notion content",
    "parameters": {
        "type": "object",
        "properties": {
            "steps": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "reasonofSimilarity": {
                            "type": "string",
                            "description": "Short Summary about how the HTML is related to my notion content"
                        },
                    },
                    "required": ["reasonofSimilarity"]
                }
            }
        },
        "required": ["step"]
    }
}]

# retrieve notion data
def get_reasons(html_content):
    # get most k most similar notion data
    notion_example_content = """When friendships sour, good friends are also courageous: they initiate hard conversations that are uncomfortable, even painful, but they do it in spite of it, because they care about their relationship with you more than their present discomfort. In good friendships, communicating your needs and holding each other accountable is a form of respect for both your friend and respect for yourself."""

    html_summarization_example = """This page discusses the importance of being a good friend to oneself, acknowledging needs, and building a positive relationship with oneself. It touches on the topics of self-respect, self-forgiveness, and the need to support oneself to become the best version of oneself."""

    reasonsofSimilarity = """This page discusses the importance of being a good friend to oneself, acknowledging needs, and building a positive relationship with oneself. It touches on the topics of self-respect, self-forgiveness, and the need to support oneself to become the best version of oneself."""

    notion_content = load_notion_data(html_content)
    notion_example_content = """When friendships sour, good friends are also courageous: they initiate hard conversations that are uncomfortable, even painful, but they do it in spite of it, because they care about their relationship with you more than their present discomfort. In good friendships, communicating your needs and holding each other accountable is a form of respect for both your friend and respect for yourself."""

    html_summarization_example = """This page discusses the importance of being a good friend to oneself, acknowledging needs, and building a positive relationship with oneself. It touches on the topics of self-respect, self-forgiveness, and the need to support oneself to become the best version of oneself."""

    reasonsofSimilarity = """This page discusses the importance of being a good friend to oneself, acknowledging needs, and building a positive relationship with oneself. It touches on the topics of self-respect, self-forgiveness, and the need to support oneself to become the best version of oneself."""


    example = openai.openai_object.OpenAIObject()
    example["role"] = "system"
    example["content"] = """You are a world class state of the art agent. Your purpose is to correctly complete this task :
    `Return a short summary about how the given content is relevant to my notion notes provide a sentence summary` These are the guidelines you consider when completing
    your task: Give One short reason for why it is relevant. If you are unsure of the answer, try to think about the reason as a whole."""
    example["role"] = "user"
    example["content"] = """Give me the reasons for the following notion: {} and the following HTML {}""".format(notion_example_content, html_summarization_example)
    example["role"] = "assistant"
    example["function_call"] = {
        "name": "get_notion_relevance",
        "arguments": json.dumps(
            {
                "steps": [{"reasonsofSimilarity": "this is similar because blah"}]
            },
            indent=2,
            ensure_ascii=False,
        ),
    }
    "You're an assistant that has access to Brian's Notion, where all of his notes and journals exist. When Brian visits a webpage, you're going to read the webpage and decide which Notion pages are the relevant. Please provide a 5 sentence summary of the overlap between the relevant Notion pages and the webpag"
    first_system_message = """You are a world class state of the art agent. Your purpose is to correctly complete this task :
    `Return a short summary about how the given content is relevant to my notion notes provide a sentence summary` These are the guidelines you consider when completing
    your task: Give One short reason for why it is relevant. If you are unsure of the answer, try to think about the reason as a whole."""
    notion_similar = load_notion_data(html_content)
    #print(notion_similar)
    notion_similar_text = notion_similar[0].metadata["text"]
    assistant_message = """Lets think step by to get the correct answer"""
    user_message = """Give me the reasons for the following notion: {} and the following HTML {}""".format(notion_similar_text, html_content)



    for notion in range(1):
        response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=[example,{"role": "system", "content": first_system_message},{"role": "user", "content": user_message}, {"role": "assistant", "content": assistant_message}],
        functions=functions,
        function_call={"name":"get_notion_relevance"}
    )
    data = response["choices"][0]["message"]

    arguments = json.loads(data["function_call"]["arguments"])
    output = []
    for step in arguments["steps"]:
        output.append(step["reasonofSimilarity"])

    #print(notion_similar[0].page_content)
    print(output, notion_similar[0].page_content)
    # Its important that this just build
    #s you request,
    # all these | operators are overloaded and all we do is compile
    # it to the openai kwargs
    # Also note that the System components are combined sequentially
    # so the order matters!
    '''
    pprint(task.kwargs, indent=3)
    for task in output:
        result =  task[0].create()
        print(result)
        #print(output[0].str, notion_example_source)
    '''

get_reasons(html_summarization_example)