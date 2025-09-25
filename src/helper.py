# Let's import the dome libraries
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter , RecursiveCharacterTextSplitter # for chunking the data
from langchain.embeddings import HuggingFaceEmbeddings # for creating embeddings
from typing import List # for type hinting
from langchain.schema import Document # for type hinting

# Lets creat a function to load the data from the pdf files
def load_pdf_files(data):
    loader = DirectoryLoader(
        data, # our data path
        glob="**/*.pdf", # becouse we want to load only the pdf file not other file and if we use *.pdf so it will load nly the pdf file wat that path if there is sub folder it will not load that files but **/* load all subfolders pdf files also.
        loader_cls=PyPDFLoader # we are using the PyPDFLoader class to load the pdf file.

    )
    documents = loader.load() # this will load all the documents from the pdf files
    return documents # return the documents


def filter_data(docs: List[Document]) -> List[Document]:
    """
    Giving a List of Document objects, return a new list of Documents
    containg only the "source" and "page_content"  metadata.
    """
    minimal_docs: List[Document] = [] # creating an empty list to store the filtered documents of type Document
    for doc in docs:
        src = doc.metadata.get("source") # getting the source of the document
        minimal_docs.append(
            Document(
                page_content=doc.page_content, # getting the content of the page
                metadata={"source": src } # getting the source of the document
            )
        )
    return minimal_docs # returning the filtered documents


# Split the documents inro the smaller chunks
def text_split(minimal_docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, # 500 consider as size of each chunk
        chunk_overlap=20, # 20 overlap between chunks
        length_function=len # function to calculate the length of the chunk
    )
    texts_chunk = text_splitter.split_documents(minimal_docs) # splitting the documents into chunks 
    return texts_chunk 


def download_hugging_face_embeddings_model():
    """
    Download and return the embedding model from Hugging Face.
    """
    model_name = "sentence-transformers/all-MiniLM-L6-v2" # model name from Hugging Face
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name # model name
    ) # loading the model
    return embeddings # returning the model