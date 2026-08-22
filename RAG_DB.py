from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from langchain.tools import tool
from langgraph.checkpoint.postgres import PostgresSaver
from dotenv import load_dotenv
import os
import speak
import path
import vector_db
import piper_voice


load_dotenv()
# Api key for Groq

api = os.getenv("GROQ_API_KEY")
# Database URI for Postgres
DB_URI = os.getenv("POSTGRES_URL")



if os.path.exists("./chroma_db"):
    # Existing vector database
    db = vector_db.load_vector_db()
    print("Existing Chroma DB loaded.")

else:
    # No vector DB → ask user for PDF
    chunked_data = path.get_project_path()

    if chunked_data:
        db = vector_db.create_vector_db(chunked_data)
        print("PDF embedded and stored.")
    else:
        db = None
        print("No PDF uploaded.")

# Create retriever
if db:
    retriever = db.as_retriever(
        search_kwargs={"k": 3}
    )
else:
    retriever = None

#User Question

"""question = name of candidate?"""

#Retrive relevant Chunks

"""doc = retriever.invoke(question)
for j in doc:
  print(j.page_content)"""

# Retriver tool

@tool
def search_pdf(query: str) -> str:
    """Search the uploaded PDF for information needed to answer
    the user's question.

    Use this tool whenever the user asks about information
    contained in the uploaded PDF, such as name, skills,
    education, projects, experience, contact details, etc.

    Args:
        query: A clear search query describing the information
               to find in the PDF."""

    if retriever is None:
        return "No PDF is currently available."

    docs = retriever.invoke(query)

    if not docs:
        return "No relevant information found."

    return "\n\n".join(
        doc.page_content
        for doc in docs
    )

# online groq llm creation
llm = ChatGroq(
    model="openai/gpt-oss-safeguard-20b",
    temperature=0,
    groq_api_key=api
)

# local llm without internet
# llm = ChatOllama(
#     model = "llama3.2",
#     temperature = 0
# )

# memory creation & Setup checkpointer for conversation persistence


with PostgresSaver.from_conn_string(DB_URI) as checkpointer:

    checkpointer.setup()

    #Agent creation
    agent = create_agent(
        model=llm,
        tools=[search_pdf],

        system_prompt="""You are an intelligent PDF assistant.
    your name is Mnemosyne (Meaning: Greek goddess/personification of memory and remembrance).
    Use the search_pdf tool when the user asks
    about information contained in the PDF.

    If the question does not require the PDF,
    you may answer normally.

    Never invent information from the PDF.""",

        checkpointer=checkpointer
    )
    # Conversation configuration

    config = {
        "configurable": {
            "thread_id": "user1"
        }
    }
    #model speak content
    Last_answer = None

    # model chat

    while True:

        question = input("\nYou: ")

        if question.lower() == "/bye":
            break
        if question.lower() == "/upload":
            chunked_data = path.get_project_path()
            if chunked_data:
                db = vector_db.store(chunked_data)
                print("PDF Uploaded...")
                #Create a Retriver
                retriever = db.as_retriever(search_kwargs={"k": 5})
            else:
                retriever = None

            continue
        if question.lower() == "/speak":
            piper_voice.speak(Last_answer)
            continue
        response = agent.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }, config=config)

        Last_answer = response["messages"][-1].content
        # print output
        print("\nMnemosyne:",Last_answer)