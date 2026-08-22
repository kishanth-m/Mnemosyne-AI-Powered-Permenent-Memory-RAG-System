from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma


def get_project_path():

    path = input("Enter the PDF path: ").strip().strip('"')

    if not path:

        return None

    loader = PyPDFLoader(path)

    data = loader.load()

    #Split text for creatinig Chunks

    Splitter = RecursiveCharacterTextSplitter(chunk_size = 500,chunk_overlap = 150)
    chunked_data = Splitter.split_documents(data)

    return chunked_data




    
    