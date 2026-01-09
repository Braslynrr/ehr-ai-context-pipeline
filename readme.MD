# Medical AI Assistant – Context Engineering Pipeline
## Overview

This project implements a context engineering pipeline that enables an AI agent to assist clinicians during medical consultations.
The system ingests Electronic Health Records (EHR), structures the information into contextual chunks, retrieves relevant data based on a clinician’s query, and generates grounded, traceable answers using a Large Language Model (LLM).

The focus of this implementation is clarity, traceability, and end-to-end functionality, rather than production-level optimization.

## System Goals

* Provide context-aware clinical answers

* Maintain traceability to the original EHR source

* Demonstrate a complete RAG-style pipeline

* Keep the system simple, explainable, and extensible

## High-Level Architecture

        EHR JSON
           │
           ▼
        [ Ingestion ]
           │
           ▼
        [ Chunking ]
           │
           ▼
        [ Context Enrichment ]
           │
           ▼
        [ Embedding ]
           │
           ▼
        [ In-Memory Vector Store ]
           │
           ▼
        [ Retrieval ]
           │
           ▼
        [ Context Builder ]
           │
           ▼
        [ LLM Agent ]
           │
           ▼
        Answer + Sources

## Core Components
### 1. Ingestion Pipeline

The ingestion pipeline loads raw EHR data in JSON format without modifying its original structure.

Responsibilities:

Load EHR files

Validate basic structure

Pass raw data to the chunking stage

Design decision:

The original EHR structure is preserved to reflect real-world constraints where data normalization is often infeasible.

### 2. Chunking Strategy

The EHR is split into semantically meaningful chunks based on clinical sections:

* Demographics

* Medical history

* Medications

* Allergies

* Visits

* Lab results

Each chunk contains:

Type of section

Optional date (for temporal data)

Human-readable text representation

Example chunk:

    Patient P001. Current medications: Metformin 850mg twice daily, Losartan 50mg once daily.


Design decision:

Chunking by clinical meaning, not by token size.

This improves interpretability and grounding.

###  3. Context Enrichment (for Embeddings)

Before embedding, each chunk is enriched with:

Temporal hints (when applicable) in spanish and english initially.

This ensures embeddings remain effective even when:

Field names and the content are in different languages

Design decision:

Enrichment is applied only to the text used for embeddings, not to the original data.

### 4. Embeddings & Vector Store

A single embedding per chunk is generated

Embeddings are stored in an in-memory vector store

Metadata (patient_id, section, date) is stored alongside vectors

Design decision:

Use of Ollama embeddings due to lack of valid API Keys

No complex embedding hierarchies

No reranking or cross-encoders

This keeps retrieval transparent and easy to debug

### 5. Retrieval

At query time:

The question is embedded

Relevant chunks are retrieved via similarity search

### 6. Context Builder

The retrieved chunks are:

* Rewritten to reduce the tokens costs without losing important information

* Merged into a structured context

This context is passed to the LLM along with the clinician’s question.

Design decision:

Context assembly is explicit and deterministic.

The LLM is not responsible for deciding relevance.

### 7. LLM Agent

The agent:

Receives the structured context

Answers the question using only the provided information

Produces grounded responses

The system supports:

Local LLM execution using Ollama

Pluggable LLM backends

## Grounding & Traceability

Every answer can be traced back to:

Section of the EHR

Visit date or lab date (when applicable)

Example:

    “According to the visit on 2024-10-15, the patient’s fasting glucose was 128 mg/dL.”

This ensures transparency and clinical safety.

# Configuration

The system is partially configurable via environment variables using a `.env` file.
This allows changing the LLM provider, model, and EHR data source without modifying
application code.

## Environment Variables

| Variable | Description |
|--------|-------------|
| MEDICAL_EHR_LOCATION | Path to the directory containing EHR JSON files |
| MEDICAL_LLM_PROVIDER | LLM provider (`ollama`, `openai`, `gemini`, etc.) |
| MEDICAL_LLM_MODEL | Model name for the selected provider |
| OPENAI_API_KEY | Required when using OpenAI |
| GOOGLE_API_KEY | Required when using Google Gemini |

## Example `.env`

```env
MEDICAL_EHR_LOCATION=E:\Python-projects\Medical-AI\data
MEDICAL_LLM_PROVIDER=ollama
MEDICAL_LLM_MODEL=qwen3:4b
```

## Switching Providers Example

To use Google Gemini:

```env
MEDICAL_LLM_PROVIDER=gemini
MEDICAL_LLM_MODEL=gemini-1.5-flash
GOOGLE_API_KEY=your_api_key_here
```


# Running the Project
## Prerequisites

- Python 3.10+
- Ollama installed locally
- The following Ollama models pulled locally:
  - `qwen3:4b` (LLM for answering questions)
  - `nomic-embed-text` (embedding model for retrieval)

## Setup

python -m venv venv

source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt

## Pull Required Ollama Models

Before running the application, make sure the required models are available locally:

```bash
ollama pull qwen3:4b
ollama pull nomic-embed-text
```


## Start Ollama

```bash
ollama run qwen3:4b
```

## Run the Application

python main.py


## The Flask API will start at:

http://127.0.0.1:5000


## API Example

POST /ask

```json
{
  "patient": "P001",
  "question": "How has the patient's glucose evolved?"
}
```

## Trade-offs & Limitations

Vector store is in-memory (non-persistent)

No advanced reranking or hybrid search

Design for demo purposes

Different LLM providers may produce slightly different answers due to model behavior, even when using the same context.

## Future Improvements

Persistent vector database

Reranking with cross-encoders

Query rewriting for complex questions

Global retrieval queries

More configurable options (Embeddings)

Access control

Audit logging

## Conclusion

This project demonstrates a complete, explainable context engineering pipeline suitable for clinical decision support.
The design prioritizes clarity, traceability, and modularity, making it easy to extend or producti