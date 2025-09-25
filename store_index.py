from dotenv import load_dotenv
import os
from src.helper import load_pdf_files, filter_data, text_split, download_hugging_face_embeddings_model
from pinecone import Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain.vectorstores import Pinecone


load_dotenv() # load the .env file


# importin the api keys
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
#OPENAI_API_KEY =os.getenv("OPENAI_API_KEY")

# We also need to set the env variable for the api keys
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
#os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


extracted_data = load_pdf_files("data") # loading the pdf files from the data folder
filtered_data = filter_data(extracted_data) # filtering the data to remove any unwanted characters
text_chunks = text_split(filtered_data) # splitting the data into smaller chunks

# Download the embeddings model from hugging face
embeddings = download_hugging_face_embeddings_model()

pinecone_api_key = PINECONE_API_KEY
pc = Pinecone(api_key=pinecone_api_key)


index_name = "medical-bot"

# Create the index if it does not exist
if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=384, # dimension of the embedding model
        metric="cosine", # metric to use for the index
        spec=ServerlessSpec( cloud="aws", region="us-east-1") # 


    )
index = pc.Index(index_name)

# Store all in the pinecone vector store
docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks, # our chunked documents
    embedding=embeddings, # our embedding model
    index_name=index_name

)