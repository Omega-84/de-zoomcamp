FROM python:3.13.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /code

ENV PATH="/code/.venv/bin:$PATH"

COPY pyproject.toml uv.lock .python-version green_tripdata_2025-11.parquet taxi_zone_lookup.csv ./

RUN uv sync --locked

COPY ingest_to_db.py .

ENTRYPOINT ["python", "ingest_to_db.py"]
