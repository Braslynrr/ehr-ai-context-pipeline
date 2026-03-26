import psycopg2
from psycopg2.extensions import connection

def get_db_connection() -> connection:
    return psycopg2.connect(
        host="localhost",
        port=5432,
        user="ehr_user",
        password="ehr_password",
        dbname="ehr_db"
    )