FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./backend
COPY services ./services
COPY ehr_ai_core ./ehr_ai_core

ENV PYTHONPATH=/app

CMD ["uvicorn", "backend.ehr_api:app", "--host", "0.0.0.0", "--port", "8000"]