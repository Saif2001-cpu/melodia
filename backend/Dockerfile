# ── Build stage ───────────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /app

RUN pip install --no-cache-dir poetry==1.8.3

COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.in-project true \
    && poetry install --only main --no-root --no-interaction

# ── Production stage ──────────────────────────────────────────────────────────
FROM python:3.11-slim AS production

WORKDIR /app

# Copy virtualenv from builder
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

COPY . .

RUN addgroup --system melodia && adduser --system --group melodia
USER melodia

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]

EXPOSE 8000

# ── Development stage ─────────────────────────────────────────────────────────
FROM python:3.11-slim AS development

WORKDIR /app

RUN pip install --no-cache-dir poetry==1.8.3

COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.in-project true \
    && poetry install --no-root --no-interaction

COPY . .
ENV PATH="/app/.venv/bin:$PATH"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

EXPOSE 8000
