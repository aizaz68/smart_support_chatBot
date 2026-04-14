import chromadb
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
load_dotenv()
DATA_PATH = "data/knowledge_base/company_info.txt"

def load_and_index_documents():
    loader = TextLoader(DATA_PATH)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    client = chromadb.HttpClient(host="localhost", port=8001)
    vectorstore = Chroma.from_documents(
        chunks,
        embeddings,
        client=client,
        collection_name="company_knowledge"
    )

    print(f"Indexed {len(chunks)} chunks.")
    return vectorstore

def load_vectorstore():
    embeddings = OpenAIEmbeddings()
    client = chromadb.HttpClient(host="localhost", port=8001)
    return Chroma(
        client=client,
        collection_name="company_knowledge",
        embedding_function=embeddings
    )

# if __name__ == "__main__":
#     load_and_index_documents()
