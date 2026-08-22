from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


#Store Embedded data into vector DB
def store(chunked_data):

    #  Embeddings

    Em_data = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    db = Chroma.from_documents(
        documents=chunked_data,
        embedding=Em_data,
        persist_directory="./chroma_db"
    )
    return db

def load_vector_db():

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )

    return db