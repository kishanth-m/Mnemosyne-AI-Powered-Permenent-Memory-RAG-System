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

<svg width="100%" viewBox="0 0 680 700" xmlns="http://www.w3.org/2000/svg" role="img">
<title>Mnemosyne end-to-end workflow</title>
<desc>A PDF is loaded, chunked and embedded into ChromaDB. When a user asks a question, the agent either retrieves relevant chunks from ChromaDB or answers directly, calls the LLM, and saves the exchange to PostgreSQL memory.</desc>
<defs>
<marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M2 1L8 5L2 9" fill="none" stroke="#5F5E5A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
</marker>
</defs>

<!-- n1 Upload PDF -->
<rect x="190" y="20" width="300" height="56" rx="10" fill="#F1EFE8" stroke="#5F5E5A" stroke-width="0.5"/>
<text x="340" y="40" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="14" font-weight="500" fill="#444441">Upload PDF</text>
<text x="340" y="58" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="12" fill="#5F5E5A">User provides a document</text>
<line x1="340" y1="76" x2="340" y2="116" stroke="#5F5E5A" stroke-width="1" marker-end="url(#arrow)"/>

<!-- n2 Load, split, embed -->
<rect x="190" y="116" width="300" height="56" rx="10" fill="#E1F5EE" stroke="#0F6E56" stroke-width="0.5"/>
<text x="340" y="136" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="14" font-weight="500" fill="#085041">Load, split &amp; embed</text>
<text x="340" y="154" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="12" fill="#0F6E56">Extract text, chunk, embed</text>
<line x1="340" y1="172" x2="340" y2="212" stroke="#5F5E5A" stroke-width="1" marker-end="url(#arrow)"/>

<!-- n3 ChromaDB -->
<rect x="190" y="212" width="300" height="56" rx="10" fill="#FAECE7" stroke="#993C1D" stroke-width="0.5"/>
<text x="340" y="232" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="14" font-weight="500" fill="#712B13">ChromaDB</text>
<text x="340" y="250" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="12" fill="#993C1D">Persistent vector store</text>
<line x1="340" y1="268" x2="340" y2="308" stroke="#5F5E5A" stroke-width="1" marker-end="url(#arrow)"/>

<!-- n4 User asks a question -->
<rect x="190" y="308" width="300" height="56" rx="10" fill="#F1EFE8" stroke="#5F5E5A" stroke-width="0.5"/>
<text x="340" y="328" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="14" font-weight="500" fill="#444441">User asks a question</text>
<text x="340" y="346" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="12" fill="#5F5E5A">Sent to the agent</text>
<line x1="340" y1="364" x2="340" y2="404" stroke="#5F5E5A" stroke-width="1" marker-end="url(#arrow)"/>

<!-- n5 Agent -->
<rect x="190" y="404" width="300" height="56" rx="10" fill="#EEEDFE" stroke="#534AB7" stroke-width="0.5"/>
<text x="340" y="424" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="14" font-weight="500" fill="#3C3489">Agent (LangChain)</text>
<text x="340" y="442" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="12" fill="#534AB7">Retrieves or answers directly</text>

<!-- feedback path: Agent -> ChromaDB (retrieval) -->
<path d="M190 432 L110 432 L110 240 L190 240" fill="none" stroke="#5F5E5A" stroke-width="1" stroke-dasharray="4 3" marker-end="url(#arrow)"/>
<text text-anchor="end" font-family="sans-serif" font-size="12" fill="#5F5E5A">
<tspan x="100" y="318">Retrieves</tspan>
<tspan x="100" y="332">chunks</tspan>
</text>

<!-- Agent <-> PostgreSQL -->
<line x1="490" y1="432" x2="515" y2="432" stroke="#5F5E5A" stroke-width="1" marker-start="url(#arrow)" marker-end="url(#arrow)"/>
<rect x="515" y="412" width="120" height="40" rx="8" fill="#E1F5EE" stroke="#0F6E56" stroke-width="0.5"/>
<text x="575" y="426" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="13" font-weight="500" fill="#085041">PostgreSQL</text>
<text x="575" y="441" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="11" fill="#0F6E56">Memory</text>

<line x1="340" y1="460" x2="340" y2="500" stroke="#5F5E5A" stroke-width="1" marker-end="url(#arrow)"/>

<!-- n6 LLM -->
<rect x="190" y="500" width="300" height="56" rx="10" fill="#E1F5EE" stroke="#0F6E56" stroke-width="0.5"/>
<text x="340" y="520" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="14" font-weight="500" fill="#085041">LLM generates answer</text>
<text x="340" y="538" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="12" fill="#0F6E56">Ollama (local) or Groq (cloud)</text>
<line x1="340" y1="556" x2="340" y2="596" stroke="#5F5E5A" stroke-width="1" marker-end="url(#arrow)"/>

<!-- n7 Response -->
<rect x="190" y="596" width="300" height="56" rx="10" fill="#F1EFE8" stroke="#5F5E5A" stroke-width="0.5"/>
<text x="340" y="616" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="14" font-weight="500" fill="#444441">Response delivered</text>
<text x="340" y="634" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="12" fill="#5F5E5A">Saved to conversation memory</text>
</svg>

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
git clone <YOUR_REPOSITORY_URL>
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

## About

Mnemosyne started as a hands-on exploration of modern generative AI application architecture — not just a PDF chatbot, but an integration exercise across retrieval, flexible LLM inference, agent tooling, persistent memory, and voice interaction, built to reflect practical, production-adjacent AI engineering patterns.

---

**Mnemosyne** — *remembers what matters.*