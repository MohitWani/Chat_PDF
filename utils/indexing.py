from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
import os
from langchain_community.embeddings import GPT4AllEmbeddings
import tempfile

#Load your docs.
def load_document(pdf_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(pdf_file.read())
        loader = PyPDFLoader(tmp_file.name)
        document = loader.load()
    print("Document Loaded successfully...")
    return document

#Split documents into chunks.
def splitter(document):
    doc_split = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap = 200,
    )

    docs_metadata = doc_split.split_documents(documents=document)

    docs = [doc for doc in docs_metadata]
    print("Chunks are created successfully...")
    return docs

#create vector store to retrieve documents.
def create_vectorstore(docs, embedding=GPT4AllEmbeddings(), path_tosave='D:/my_projects/ScholarQuery/assignment'):

    vectorstore = FAISS.from_documents(docs, embedding)

    path = path_tosave
    folder = "faiss_index"

    persist_db = os.path.join(path, folder)
    os.makedirs(persist_db, exist_ok=True)

    vectorstore.save_local(persist_db)
    return "Vector database is Saved."

