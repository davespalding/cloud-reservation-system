FROM python:3.12-alpine AS builder

RUN pip install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-interaction && rm -rf $POETRY_CACHE_DIR

FROM python:3.12-alpine AS runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY pdfgen/*.py /pdfgen/
COPY pdfgen/config.yaml /pdfgen/

EXPOSE 8891

ENTRYPOINT ["python", "-m", "pdfgen"]