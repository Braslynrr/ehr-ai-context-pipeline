from typing import Optional

from psycopg2.extensions import connection, cursor
from psycopg2.extras import Json
from ehr_ai_core.error.app_error import AppError
from ehr_ai_core.retrieval.IVector_db import IVector
from ehr_ai_core.retrieval.vector_entry import VectorEntry
from ehr_ai_core.db_conection import get_db_connection

class Postgress_db(IVector):

    __conn: Optional[connection] = None

    def __init__(self):
        super().__init__()
        self.__conn = get_db_connection()

    def add(self, entries: list[VectorEntry] | VectorEntry):
        cursor = None
        try:
            cursor = self.__conn.cursor()

            if isinstance(entries, list):
                for entry in entries:
                    self.__upsert_chunk(entry, cursor)
            else:
                self.__upsert_chunk(entries, cursor)

            self.__conn.commit()

        except Exception as e:
            self.__conn.rollback()
            raise AppError(f"Error inserting embeddings: {e}", 500)

        finally:
            if cursor:
                cursor.close()
    
    def clean(self):
        cursor = self.__conn.cursor()
        cursor.execute("""DELETE FROM chunks""")
        cursor.close()
        
    def search(self, query_embedding: list[float], k=2, patient_id: str | None = None):
        cursor = None
        try:
            cursor = self.__conn.cursor()

            base_query = """
                SELECT id, patient_id, type, content, date, source,
                    1 - (embedding <=> %s::vector) AS similarity
                FROM chunks 
            """

            params = [query_embedding]

            if patient_id:
                base_query += "WHERE patient_id = %s"
                params.append(patient_id)

            base_query += " ORDER BY embedding <=> %s::vector LIMIT %s"
            params.extend([query_embedding, k])

            cursor.execute(base_query, tuple(params))
            results = cursor.fetchall()

            return [self.__map_row_to_chunk(match) for match in results]

        except Exception as e:
            raise AppError(f"Error searching embeddings: {e}", 500)

        finally:
            if cursor:
                cursor.close()

    def __upsert_chunk(self, entry: VectorEntry, cursor:cursor):
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

    def __map_row_to_chunk(self, row):
        return {
            "id": row[0],
            "patient_id": row[1],
            "type": row[2],
            "content": row[3],
            "date": row[4],
            "source": row[5],
            "similarity": row[6]
        }
    
    def _map_patient_to_chunk(self, row) -> dict:
        patient = row[1]
        patient["patient_id"] = row[0]
        return patient
    
    def get_patients(self, id_list:list[str] | None = None)-> list[dict]:
        cursor = self.__conn.cursor()
        params = []

        query = """
            SELECT patient_id, content
            FROM chunks
            WHERE type = 'demographics'"""
        
        if id_list and len(id_list) > 0:
            placeholders = ','.join(['%s'] * len(id_list))
            query += f"and patient_id IN ({placeholders})"
            params.extend(id_list)

        cursor.execute(query, tuple(params))

        results = cursor.fetchall()

        return [self._map_patient_to_chunk(patient) for patient in results]
    
    def chunks_count(self, patient_id = None):
        cursor = self.__conn.cursor()
        params = []

        query = """
            SELECT count(id)
            FROM chunks
            """
        
        if patient_id:
            query += "WHERE patient_id = %s"
            params.append(patient_id)

        cursor.execute(query, tuple(params))

        results = cursor.fetchone()

        return results[0]