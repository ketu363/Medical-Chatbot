from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings_model
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI



from dotenv import load_dotenv
from src.prompt import *
import os


# First we will initialize the flask app
app = Flask(__name__)


load_dotenv() # load the .env file

# importin the api keys
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
#OPENAI_API_KEY =os.getenv("OPENAI_API_KEY")
# We also need to set the env variable for the api keys
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
#os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Above open api key is commented becouse we are using the azure openai key
# So we will set the azure openai key here
azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
os.environ["AZURE_OPENAI_API_KEY"] = azure_api_key
chatModel = AzureChatOpenAI(
    deployment_name="gpt-35-turbo",
    openai_api_version="2023-12-01-preview",
    azure_endpoint="https://genaiassistantprudential.openai.azure.com",
    api_key=azure_api_key  # works now
)


# Now we want to load the embedding model becouse we want to loead the our existing index
embeddings = download_hugging_face_embeddings_model()

index_name = "medical-bot"
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

# retrieve the data from the pinecone index
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3}) # k is the number of documents to retrieve
# Intitializing the openai chat model (we already intialized the chat model above)
#chatModel = AzureChatOpenAI(deployment_name="gpt-35-turbo")
# Creting thr prompt
prompt = ChatPromptTemplate.from_messages( # creating the prompt template
    [
        ("system", system_prompt), # system message
        ("human", "{input}"), # human message
    ]
)

# Creating teh RAG chain
question_answering_chain = create_stuff_documents_chain(chatModel, prompt)
reg_chain = create_retrieval_chain(retriever,
                                   question_answering_chain)

# nOW APP is initiallized now we will create the bacic routes
# So this will be the defoult rout which will render the chat.html file 


@app.route("/")
def index():
    return render_template("chat.html")

# We will create a new route for the chat functionality
# So whenever the user sends a message we will handle it here
@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form.get("msg") # get the message from the request
    input = msg # what evert the user is sending msg we getting there in the input
    print(input)
    # Now we will pass the message
    response = reg_chain.invoke({"input": msg}) # then we executing the input in rag chain
    print("Response: ", response["answer"])
    return str(response["answer"]) # returning the response as a string

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)