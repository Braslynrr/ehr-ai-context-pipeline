CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE patients (
    id TEXT PRIMARY KEY,
    name TEXT,
    blood_type TEXT,
    gender TEXT,
    age INTEGER
);

CREATE TABLE chunks (
    id TEXT PRIMARY KEY,
    patient_id TEXT REFERENCES patients(id),
    type TEXT,
    content JSONB,
    date DATE,
    source TEXT,
    embedding VECTOR(1024)
);.