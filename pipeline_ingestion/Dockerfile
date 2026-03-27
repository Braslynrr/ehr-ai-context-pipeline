FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY pipeline_ingestion ./pipeline_ingestion
COPY ehr_ai_core ./ehr_ai_core
COPY services ./services
COPY data ./input

CMD ["python", "-m", "pipeline_ingestion.app"]