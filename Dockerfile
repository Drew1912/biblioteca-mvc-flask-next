FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

COPY pyproject.toml .
COPY main.py .
COPY app ./app
COPY tests ./tests

RUN pip install ".[dev]"

CMD ["flask", "--app", "main:create_app", "run", "--host=0.0.0.0", "--port=5000"]