CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE patients (
    id TEXT PRIMARY KEY,
    name TEXT
);

CREATE TABLE ehr_documents (
    id SERIAL PRIMARY KEY,
    patient_id TEXT REFERENCES patients(id),
    raw_json JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE chunks (
    id TEXT PRIMARY KEY,
    patient_id TEXT,
    type TEXT,
    content JSONB,
    date DATE,
    source TEXT,
    embedding VECTOR(768)
);.