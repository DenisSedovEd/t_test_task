FROM python:3.13-slim AS builder

RUN apt-get update && apt-get install -y build-essential libsqlite3-dev && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

ENV UV_LINK_MODE=copy
RUN uv sync --frozen

COPY app ./app
COPY . .

FROM python:3.13-slim

WORKDIR /app

COPY --from=builder /app/.venv /.venv

COPY --from=builder /app /app

ENV PATH="/.venv/bin:$PATH" \
    PYTHONPATH="/app" \
    UV_PYTHON_DOWNLOADS=never

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]