from dotenv import load_dotenv
from app.rag.retriever import retrieve_relevant_docs
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
load_dotenv()

def augment(query:str,docs:list)-> list:
    context="\n\n".join([doc['content'] for doc in docs])
    return [
        SystemMessage(content=f"""
You are a helpful support agent for ScalableTech Solutions.
Use ONLY the context below to answer the user's question.
If the answer is not in the context, say you don't know.

Context:
{context}
"""),
HumanMessage(content=query)
    ]

def generate(messages:list)-> str:
    llm=ChatOpenAI(model="")

if __name__ == "__main__":
    print('i ma here ')