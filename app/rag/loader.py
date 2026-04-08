from langchain_community.document_loaders import  TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import os
from dotenv import load_dotenv
load_dotenv()
DATA_PATH="data/knowledge_base/company_info.txt"
VECTORSTORE_PATH= "db/chroma_index"

def load_and_index_documents():
    #check if already exits
    if os.path.exists(VECTORSTORE_PATH):
        print('Already Exits, Skipping Indexing....')
        return load_vectorstore()

    #Load
    loader=TextLoader(DATA_PATH)
    documents=loader.load()

    #chunk
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks=splitter.split_documents(documents)

    #Embed + Store
    embedding=OpenAIEmbeddings()
    vectorstores=Chroma.from_documents(chunks,embedding,persist_directory=VECTORSTORE_PATH)
    print(f"Indexed {len(chunks)} chunks")

    return vectorstores

def load_vectorstore():
    embeddings=OpenAIEmbeddings()
    return Chroma(
        persist_directory=VECTORSTORE_PATH,
        embedding_function=embeddings
    )

