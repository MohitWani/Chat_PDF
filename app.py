import streamlit as st
from utils.indexing import *
from utils.retrieval import *
from utils.generation import *
from io import BytesIO

#title of Page
st.title("Chat with your PDF docs using Resoning and Action Prompt")

#Upload your files.
uploaded_file = st.file_uploader("Choose a PDF files", type="pdf", accept_multiple_files=True)

#Perform RAG operations.
if uploaded_file is not None:
    all_split_docs = []
    for file in uploaded_file:
        pdf_bytes = BytesIO(file.read())
        document = load_document(pdf_bytes)
        doc_split = splitter(document)
        all_split_docs.extend(doc_split)

    if all_split_docs:
        create_vectorstore(all_split_docs)

    #If query is available then perform retrieval.
    query = st.text_input("Ask query to document.")
    if query:
        embedding = GPT4AllEmbeddings()
        db = FAISS.load_local('D:/my_projects/ScholarQuery/assignment/faiss_index', embedding, allow_dangerous_deserialization=True)
        retrieval = db.as_retriever()
        llm = model()
        response = Naive_retriever(llm, retrieval, query)
        
        st.write(response)
    
    





