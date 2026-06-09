FROM ghcr.io/astral-sh/uv:python3.13-bookworm AS builder

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev --frozen

COPY . .
RUN uv run python manage.py collectstatic --noinput


FROM python:3.13-slim-bookworm

RUN groupadd -r django && useradd -r -g django django

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/static /app/static
COPY --from=builder /app /app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN mkdir -p /app/data /app/media && chown -R django:django /app

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["gunicorn", "spicesminsk.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
