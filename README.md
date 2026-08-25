# Mnemosyne

### A Private, Local-First AI Knowledge Assistant with Persistent Memory

> Named after the Greek goddess of memory — an AI that doesn't just answer, it remembers.

Mnemosyne is a **Retrieval-Augmented Generation (RAG)** assistant that lets you have real conversations with your own documents. Upload a PDF, ask questions in plain language, and get answers grounded in the actual content — not hallucinated guesses. Conversations persist across sessions, the LLM backend is your choice of local or cloud, and you control where your data lives.

---

## Why Mnemosyne Exists

Most chatbots have three recurring gaps:

- They don't know what's inside your private documents.
- They forget everything the moment you close the app.
- They send your data to someone else's server to get an answer.

Mnemosyne closes all three gaps in one system: **Vector Search + Flexible LLM Inference + Durable Memory + Voice Output.**

---

## What It Does

**Ask your documents anything.**
Upload a PDF and query it conversationally. Mnemosyne retrieves the relevant passages before generating a response, so answers stay grounded in your source material instead of the model's imagination.

```text
You: What skills does the candidate have?
Mnemosyne: Based on the uploaded document, the candidate has experience with...
```

**Understand meaning, not just keywords.**
Documents are chunked, embedded, and stored in a vector database (ChromaDB), so retrieval is based on semantic similarity — the system finds the right passage even if your question doesn't share exact wording with the source text.

**Choose your own LLM backend.**
Mnemosyne works with either a fully local model (Llama 3.2 via Ollama, for zero external dependency and full data privacy) or a fast cloud-hosted model (Groq API), switchable with a one-line change — so you can trade off privacy versus speed depending on the situation.

**Remember across sessions.**
Conversation state is checkpointed to PostgreSQL via LangGraph, so context survives restarts — not just within a single chat window.

```text
You: My name is Alex.
Mnemosyne: Nice to meet you, Alex!

--- (restart the app) ---

You: What is my name?
Mnemosyne: Your name is Alex.
```

**Decide when to use the document vs. general knowledge.**
Mnemosyne is built as a LangChain agent with a dedicated `search_pdf` tool. The agent decides on its own whether a question needs document retrieval or can be answered directly — it isn't a rigid, hardcoded if/else.

**Talk back.**
Optional text-to-speech via Piper TTS reads the assistant's last response aloud on command.

---

## How It's Built

From uploading a PDF to getting a spoken-ready answer, this is the full path a question takes through the system:

```mermaid
flowchart TD
    A[Upload PDF]:::start --> B[Load, split & embed]:::process
    B --> C[(ChromaDB<br/>vector store)]:::store
    D[User asks a question]:::start --> E{Agent}:::agent
    E -- retrieves chunks --> C
    E <--> F[(PostgreSQL<br/>memory)]:::process
    E --> G[LLM generates answer<br/>Ollama or Groq]:::process
    G --> H[Response delivered]:::start

    classDef start fill:#F1EFE8,stroke:#5F5E5A,color:#2C2C2A;
    classDef process fill:#E1F5EE,stroke:#0F6E56,color:#085041;
    classDef store fill:#FAECE7,stroke:#993C1D,color:#712B13;
    classDef agent fill:#EEEDFE,stroke:#534AB7,color:#3C3489;
```

---

## Tech Stack

| Layer                  | Technology                                    |
| ----------------------- | ---------------------------------------------- |
| Agent orchestration      | LangChain, LangGraph                           |
| LLM backend               | Ollama (Llama 3.2, local) or Groq API (cloud)  |
| Vector store               | ChromaDB                                      |
| Embeddings                  | HuggingFace `sentence-transformers`            |
| Document ingestion           | PyPDFLoader                                   |
| Persistent memory              | PostgreSQL + LangGraph checkpointer            |
| Voice output                     | Piper TTS / pyttsx3 / SoundDevice              |
| Dependency management              | `uv`                                          |

---

## Project Structure

```text
Mnemosyne/
│
├── .env.example
├── .gitignore
├── .python-version
│
├── RAG_DB.py                # Application entry point & chat loop
├── path.py                  # PDF loading and chunking
├── vector_db.py              # ChromaDB vector store operations
│
├── speak.py                   # Text-to-speech implementation
├── piper_voice.py              # Piper voice functionality
│
├── check_memory.sql             # Inspect/reset PostgreSQL memory
│
├── README.md
│
├── pyproject.toml
└── uv.lock
```

---

## Getting Started

### 1. Clone and install

```bash
git clone https://github.com/kishanth-m/Mnemosyne-AI.git
cd Mnemosyne
uv sync
```

### 2. Choose your LLM backend

**Option A — Local (Ollama + Llama 3.2):** fully private, no external API calls.

```bash
ollama pull llama3.2
```
Make sure the Ollama service is running before starting the app.

**Option B — Cloud (Groq API):** faster inference, no local GPU required.

Just supply a `GROQ_API_KEY` in your `.env` (see below) and point the LLM initialization at Groq instead of Ollama.

### 3. Configure environment variables

Copy `.env.example` to `.env` and fill in your own values:

```env
GROQ_API_KEY=your_api_key_here
POSTGRES_URL=your_postgresql_connection_string
```

> `.env` is git-ignored — never commit real credentials. Only set `GROQ_API_KEY` if you're using the cloud backend.

### 4. Set up PostgreSQL

Create a database and point `POSTGRES_URL` at it:

```text
postgresql://username:password@localhost:5432/database_name
```

The LangGraph checkpointer creates the required tables automatically on first run.

### 5. Run it

```bash
uv run RAG_DB.py
```

---

## Commands

| Command   | What it does                       |
| --------- | ----------------------------------- |
| `/upload` | Upload and embed a new PDF          |
| `/speak`  | Read the last response aloud        |
| `/bye`    | Exit                                 |

---

## Example Session

```text
You: /upload
Enter the PDF path: C:\Documents\resume.pdf
Mnemosyne: PDF uploaded and embedded successfully.

You: What technical skills does the candidate have?
Mnemosyne: Based on the uploaded document, the candidate has experience with...

You: My name is Kishanth.
Mnemosyne: Nice to meet you!

You: What is my name?
Mnemosyne: Your name is Kishanth.
```

---

## Security & Privacy

Mnemosyne is built local-first: your documents, embeddings, and conversation history stay on infrastructure you control. Secrets are loaded from environment variables and never hardcoded.

Never committed to version control:
```text
.env
.venv/
chroma_db/
__pycache__/
```

`.env.example` documents the required variables without exposing real values.

---

## What This Project Demonstrates

- Retrieval-Augmented Generation (RAG) architecture
- Vector embeddings and semantic search
- Agent + tool design with LangChain
- Flexible LLM inference (local Ollama or cloud Groq)
- Persistent, cross-session conversation memory with LangGraph + PostgreSQL
- Environment-based secret management
- Text-to-speech integration
- Modern Python dependency management with `uv`

---

## Roadmap — open for contributors

None of the following is built yet — these are directions the project could grow in, and pull requests are genuinely welcome. If you pick one up, open an issue first so effort doesn't overlap.

- Web-based UI
- Speech-to-text input
- Multi-user support with authentication
- Multi-document knowledge bases
- Source citations in responses
- Streaming responses
- Hybrid (keyword + vector) retrieval
- Docker containerization / cloud deployment
- RAG evaluation and observability tooling

---
## Collaboration 

Pair programming with Spartanz.

---

## About

Mnemosyne started as a hands-on exploration of modern generative AI application architecture — not just a PDF chatbot, but an integration exercise across retrieval, flexible LLM inference, agent tooling, persistent memory, and voice interaction, built to reflect practical, production-adjacent AI engineering patterns.

---

**Mnemosyne** — *remembers what matters.*