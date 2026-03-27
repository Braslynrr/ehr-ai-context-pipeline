from typing import Optional

from psycopg2.extensions import connection
from psycopg2.extras import Json
from ehr_ai_core.retrieval.IVector_db import IVector
from ehr_ai_core.retrieval.vector_entry import VectorEntry
from ehr_ai_core.db_conection import get_db_connection

class Postgress_db(IVector):

    __conn: Optional[connection] = None

    def __init__(self):
        super().__init__()
        self.__conn = get_db_connection()

    def add(self, entry: VectorEntry):
        self.__upsert_chunk(entry)
    
    def add(self, entries: list[VectorEntry]):
        for entry in entries:
            self.__upsert_chunk(entry)
    
    def clean(self):
        cursor = self.__conn.cursor()
        cursor.execute("""DELETE FROM chunks""")
        cursor.close()
        
    def search(self, query_embedding: list[float], k=2, patient_id: str | None = None) -> dict:
        cursor = self.__conn.cursor()

        base_query = """
            SELECT id, patient_id, type, content, date, source,
                1 - (embedding <=> %s::vector) AS similarity
            FROM chunks
        """

        params = [query_embedding]

        if patient_id:
            base_query += " WHERE patient_id = %s"
            params.append(patient_id)

        base_query += " ORDER BY embedding <=> %s::vector LIMIT %s"
        params.extend([query_embedding, k])

        cursor.execute(base_query, tuple(params))

        results = cursor.fetchall()
        cursor.close()
        return [self.__map_row_to_chunk(match) for match in results]

    def __upsert_chunk(self, entry: VectorEntry):
        cursor = self.__conn.cursor()

        cursor.execute("""
        INSERT INTO chunks (id, patient_id, type, content, date, source, embedding)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id)
        DO UPDATE SET
            patient_id = EXCLUDED.patient_id,
            type = EXCLUDED.type,
            content = EXCLUDED.content,
            date = EXCLUDED.date,
            source = EXCLUDED.source,
            embedding = EXCLUDED.embedding
        """, (
            entry.payload["chunk_id"],
            entry.payload["patient_id"],
            entry.payload["type"],
            Json(entry.payload["content"]),
            entry.payload.get("date", None),     
            entry.payload.get("source", "unknown"), 
            entry.embedding
        ))

        self.__conn.commit()
        cursor.close()

    def __map_row_to_chunk(self, row):
        return {
            "id": row[0],
            "patient_id": row[1],
            "type": row[2],
            "content": row[3],
            "date": row[4],
            "source": row[5],
        }
    
    def _map_patient_to_chunk(self, row):
        patient = row[1]
        patient["patient_id"] = row[0]
        return patient
    
    def get_patients(self)-> list[tuple]:
        cursor = self.__conn.cursor()

        query = """
            SELECT patient_id, content
            FROM chunks
            WHERE type = 'demographics'
        """

        cursor.execute(query)

        results = cursor.fetchall()

        return [self._map_patient_to_chunk(patient) for patient in results]