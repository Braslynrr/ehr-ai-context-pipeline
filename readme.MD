# EHR AI Assistant – Context Engineering Pipeline

[![ci-cd](https://github.com/Braslynrr/ehr-ai-context-pipeline/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Braslynrr/ehr-ai-context-pipeline/actions/workflows/ci-cd.yml)
[![test](https://github.com/Braslynrr/ehr-ai-context-pipeline/actions/workflows/test.yml/badge.svg)](https://github.com/Braslynrr/ehr-ai-context-pipeline/actions/workflows/test.yml)

## Overview

This project implements an end-to-end AI-powered clinical assistant built on a context engineering pipeline.

It evolved from a simple RAG prototype into a modular, containerized system with:

- Retrieval-Augmented Generation (RAG)
- Streaming responses (Server-Sent Events)
- Persistent vector storage (PostgreSQL + pgvector)
- Redis-based orchestration for streaming
- Local LLM inference using Ollama
- React frontend for real-time interaction

The system is designed for clarity, traceability, and incremental evolution toward agent-like behavior.

## System Goals

* Provide context-aware clinical answers

* Maintain traceability to the original EHR source

* Demonstrate a complete RAG-style pipeline

* Keep the system simple, explainable, and extensible

## High-Level Architecture

        React Frontend
               │
               ▼
        FastAPI Backend
               │
       ┌───────┼────────┐
       ▼       ▼        ▼
   Redis     Postgres   Ollama
 (actions)  (pgvector)   (LLM)


## Infrastructure

The system is fully containerized using Docker Compose.

Services:

- `ehr_frontend` → React + Vite
- `ehr_backend` → FastAPI API layer
- `ehr_postgres` → PostgreSQL with pgvector
- `ehr_ollama` → Local LLM inference
- `ehr_redis` → Streaming coordination

This allows reproducible local environments and simplifies deployment.


## Core Components
### 1. Ingestion Pipeline

The ingestion pipeline loads raw EHR data in JSON format without modifying its original structure.

Responsibilities:

* Load EHR files

* Validate basic structure

* Pass raw data to the chunking stage

Design decision:

* The original EHR structure is preserved to reflect real-world constraints where data normalization is often infeasible.

* Ingestion performs minimal validation only. Any missing or optional fields are handled downstream to avoid early failures
and to reflect real-world incomplete medical records.

* Ingestion is performed on demand based on user selection. When a clinician selects a different patient, the previously ingested EHR is discarded
and a new ingestion pipeline is executed.

### 2. Chunking Strategy

The JSON EHR is split into semantically meaningful chunks based on clinical sections:

* Demographics

* Medical history

* Current Medications

* Chronic Conditions

* Allergies

* Visits

* Lab results

Each chunk contains:

* Type of section

* Optional date

* Human-readable text representation

Example chunk:

```json
   {
   "type": "recent_visit",
   "content": "Fasting glucose: 128 mg/dL. Blood pressure: 135/85. Losartan dosage adjusted.",
   "date": "2024-10-15",
   "doctor": "Dra. Martínez",
   "source": "Appointment (2024-10-15) with Dra. Martínez"
   }
```

Note: Example content may appear in Spanish or English, reflecting real-world EHR variability.

* Design decision:

* Chunking by clinical meaning, not by token size.
This improves interpretability and grounding.

* Chunking is defensive by design.
Missing fields do not cause failures; instead, chunks are generated using
only the available information.

This ensures robustness when working with partial or sparse EHR data.

### 3. Context Enrichment (for Embeddings)

Before embedding, each chunk is enriched with lightweight semantic hints
based on its clinical section.

This compensates for sections that lack sufficient standalone context
(e.g. lab results, visits) and improves embedding quality without modifying
the original data.

This ensures embeddings remain effective even when:

* Field names and the content are in different languages

* The content lacks sufficient contextual information for reliable embedding similarity

Design decision:

* Enrichment is applied only to the text used for embeddings, not to the original data.

* Enrichment is implemented using a static, explicit section-to-hint mapping
  (bilingual Spanish/English). This approach avoids dynamic or model-driven
  enrichment, favoring transparency and reproducibility.

* The mapping is intentionally embedded in code for this exercise but could
  be externalized in a real deployment.

In real-world EHRs, clinical content may appear in different languages or
lack sufficient context on its own. Semantic enrichment bridges this gap
by injecting bilingual contextual hints.

For example, the section type `recent_visit` is enriched using:

```json
{
  "recent_visit": {
    "es": "visita reciente",
    "en": "recent visit"
  }
}
```

### 4. Embeddings & Retrieval

- Embeddings are generated using Ollama (`bge-m3`)
- Stored in PostgreSQL using pgvector
- Retrieval is performed via vector similarity search

#### 4.1 Reranking

A lightweight reranking step has been introduced to improve relevance after retrieval.

This enhances answer quality without introducing heavy cross-encoder dependencies.

### 5. Retrieval

At query time:

* The question is embedded

* Relevant chunks are retrieved via similarity search and re-ranking

Design decision:

The retriever currently returns a dynamic number based on the amount of available chunks.

This was chosen intentionally:
- It reduces noise in the LLM context
- Improves traceability
- Keeps the system deterministic and explainable
- Empirically works well for the supported clinical queries

Dynamic chunk selection is intentionally deferred.

### 6. Context Builder

The retrieved chunks are:

* Rewritten to reduce token costs without losing important information

* Merged into a structured context

This context is passed to the LLM along with the clinician’s question.

Design decision:

* Context assembly is explicit and deterministic.

* The LLM is not responsible for deciding relevance.

* The context builder is intentionally simple.
Its responsibility is formatting and token reduction, not interpretation.

* Recursive formatting is supported to handle nested structures deterministically.


### 7. LLM Agent

The agent:

* Receives the structured context

* Answers the question using only the provided information

* Produces grounded responses

The system supports:

* Local LLM execution using Ollama

* Pluggable LLM backends

### 8. API Layer

The system exposes a minimal HTTP API using Fast Api.


### 9. Frontend

The React frontend provides:

- Real-time chat interface
- Streaming responses
- Error handling and state management
- Patient-based context interaction

Built with:

- React
- Vite
- TailwindCSS

## 10. Streaming Responses

The system supports real-time streaming of LLM responses using Server-Sent Events (SSE).

Flow:

1. Client sends query → `/ask`
2. Backend stores request in Redis
3. Client connects via SSE → `/ask/stream/{id}`
4. Backend streams LLM tokens progressively

This improves perceived performance and user experience.


## Grounding & Traceability

Every answer can be traced back to:

* Section of the EHR

* Visit date or lab date (when applicable)

Example:

    “According to the visit on 2024-10-15, the patient’s fasting glucose was 128 mg/dL.”

This ensures transparency and clinical safety.

## Testing Strategy

The system is covered by unit tests focusing on deterministic behavior:

- Ingestion tests validate file loading and structure handling
- Chunking tests ensure correct chunk generation under partial data
- Enrichment tests verify that semantic context is added when expected
- Retrieval tests validate similarity-based selection functionality
- RAG service tests validate end-to-end flow with mocked components

Non-deterministic components (LLMs, embeddings) are tested indirectly
or mocked to preserve reproducibility.

The goal of testing is correctness and robustness, not model quality.


## GitHub Actions

### CI/CD

GitHub Actions is used for:

- Running unit tests
- Building Docker images
- Injecting environment variables dynamically

The `.env` file is not committed and is instead generated during the CI pipeline.

## EHR Data Format

This project expects EHR files to follow a predefined JSON structure.
Example EHR files are available in the `data/` directory and are used
throughout the provided examples.

The schema is intentionally simple and designed for demonstration purposes.

## Configuration

Environment variables are required for service communication.

### Example `.env`

```env
MEDICAL_EHR_LOCATION=%projectDir%\data
MEDICAL_LLM_PROVIDER=ollama
MEDICAL_LLM_MODEL=llama3
EMBEDDING_MODEL=bge-m3
JWT_SECRET_KEY=<your secret key>
JWT_ALGORITHM=HS256

SAME_SITE=lax
CORS_ORIGIN=http://localhost:5173

DB_HOST=localhost
DB_PORT=5432
DB_USER=ehr_user
DB_PASSWORD=ehr_password
DB_NAME=ehr_db

OLLAMA_URL=http://localhost:11434
OLLAMA_GENERATE_URL=http://localhost:11434/api/generate

VITE_EHR_API_URL=http://localhost:8000/api

REDIS_HOST=localhost
REDIS_PORT=6379
```

### Switching Providers Example

To use Google Gemini:

```env
MEDICAL_LLM_PROVIDER=gemini
MEDICAL_LLM_MODEL=gemini-1.5-flash
GOOGLE_API_KEY=your_api_key_here
```

## Running the Project

### Start the System
   docker compose up --build

This will start:

* Backend (FastAPI)
* Frontend (React)
* PostgreSQL (pgvector)
* Redis
* Ollama

### Access the Application
- Frontend → http://localhost:5173
- Backend API → http://localhost:8000

### First Run Notes
Ollama will automatically download required models if not present
Initial startup may take longer due to model loading

### Stop the System
   docker compose down

## ⚠️ Alternative: Manual Setup (Advanced)

This project can be run without Docker, but requires manual setup of:

- Python environment
- PostgreSQL + pgvector
- Redis
- Ollama

This approach is not recommended unless you need full control over each service.


### API Request Example

POST /ask

```json
{
  "patient": "P001",
  "question": "How has the patient's glucose evolved?"
}
```

## Examples

See the following real execution examples using the full pipeline and a local LLM:

- [Medication query (English)](examples/medication_query.md)
- [Recent visit query (English)](examples/recent_visit_query.md)
- [Consulta clínica en español](examples/spanish_clinical_query.md)

Notes:
- No language-specific prompt tuning or routing was applied
- The response is fully driven by retrieved EHR context
- The same pipeline is used for all languages

## Trade-offs & Limitations

- The provided EHR data is fully synthetic and written in Spanish to avoid the use of real patient information.
- Design for demo purposes
- Interfaces and abstractions were intentionally minimized, as they were not required for the core functionality.
- No large architectural patterns (e.g., repositories, ports/adapters) were introduced to avoid unnecessary complexity.
- Different LLM providers may produce slightly different answers due to model behavior, even when using the same context.
- CI runs unit tests only and docker compose, however it won't be deployed.

## Future Improvements

- Agent-like behavior (multi-step reasoning)
- Tool usage (EHR updates, structured queries)
- Query planning and decomposition
- Memory and session persistence
- Advanced reranking strategies
- Audit logging

## Conclusion

This project demonstrates a complete, explainable context engineering pipeline
for medical question answering.

It prioritizes clarity, traceability, and modularity over optimization, making
it suitable as a reference architecture for clinical RAG systems, educational
purposes, or early-stage prototypes.

Based on empirical experimentation, the results show that model size is not a
critical factor as long as the RAG pipeline retrieves accurate and relevant
context. Even when using a relatively small local model via Ollama (~1.2 GB),
the system was able to generate coherent and medically meaningful answers when
the retrieved information was correct.
