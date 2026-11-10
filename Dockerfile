FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app app
COPY data/knowledge data/knowledge
COPY data/eval data/eval

ENV PYTHONUNBUFFERED=1
ENV HOST=0.0.0.0
RUN python -m app.main ingest

EXPOSE 7860
CMD ["python", "-m", "app.main", "ui"]
