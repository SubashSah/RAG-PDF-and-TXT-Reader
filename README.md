# RAG PDF/TXT Reader



## Features

- Upload PDF and TXT documents
- Two selectable chunking strategies
- Generate embeddings using HuggingFace
- Store embeddings in Qdrant
- Custom Conversational RAG (without RetrievalQAChain)
- Redis-based chat memory
- LLM-powered interview booking
- Store interview bookings in SQLite
- Store document metadata in SQLite

---

## Project Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd RAG-PDF-Reader
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root and add the following:

```env
GROQ_API_KEY=your_groq_api_key

QDRANT_HOST=localhost
QDRANT_PORT=6333

REDIS_URL=redis://localhost:6379
```

---

## Run Required Services

### Qdrant

```bash
docker run -d --name qdrant -p 6333:6333 qdrant/qdrant
```

### Redis Stack

```bash
docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack
```

---

## Run the Application

```bash
uvicorn app.main:app --reload
```

The application will be available at:

```
http://127.0.0.1:8000
```

Swagger API documentation:

```
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Upload Document

**POST**

```
/documents/upload
```

Supports:

- PDF
- TXT

Chunking strategies:

- recursive
- character

---

### Chat

**POST**

```
/chat
```

Example request:

```json
{
    "session_id": "user1",
    "question": "What is the uploaded document about?"
}
```

---

## Project Structure

```
app/
├── api/
├── services/
├── enums.py
├── schemas.py
└── main.py

uploads/
requirements.txt
README.md
```

## Technologies Used

- FastAPI
- LangChain
- Groq
- HuggingFace Embeddings
- Qdrant
- Redis
- SQLite