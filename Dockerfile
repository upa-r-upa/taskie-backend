FROM python:3.11.7-slim

WORKDIR /source

COPY poetry.lock pyproject.toml /source/

RUN pip install --no-cache-dir poetry==1.8.0

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi --without dev

COPY app/ app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]