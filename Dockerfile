FROM python:3.11.7-slim

WORKDIR /source
RUN mkdir -p /source/db

COPY poetry.lock pyproject.toml /source/

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false
RUN poetry install --only main --no-interaction --no-ansi

COPY app/ app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]