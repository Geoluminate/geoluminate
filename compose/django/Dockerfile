FROM python:3.11-slim-bullseye as builder

RUN apt-get update && \
    pip install poetry && \
    poetry self add poetry-plugin-bundle && \
    apt-get install --no-install-suggests --no-install-recommends

WORKDIR /app
COPY . .
RUN poetry bundle venv --only=main /venv

FROM geoluminate/geoluminate:latest AS run-stage

COPY --from=builder /venv /venv
