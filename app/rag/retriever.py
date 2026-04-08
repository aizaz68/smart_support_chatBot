from app.rag.loader import load_vectorstore
def retrieve_relevant_docs(query:str)-> list[str]:
    db=load_vectorstore()
    results=db.similarity_search(query,k=4)

    docs=[]
    for doc in results:
        docs.append({
            "content":doc.page_content,
            "source":doc.metadata.get('source','unknown')
        })
    return docs


# if __name__ == "__main__":
#     docs=retrieve_relevant_docs('which services you provide?')
#     for doc in docs:
#         print(doc)
#         print('\n\n\n\n')

