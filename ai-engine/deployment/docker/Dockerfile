FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
ENV PYTHONPATH=/app
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install \
        --no-cache-dir \
        --index-url https://download.pytorch.org/whl/cpu \
        torch==2.3.1 && \
    grep -v '^torch' requirements.txt > requirements-docker.txt && \
    pip install \
        --no-cache-dir \
        -r requirements-docker.txt

COPY . .

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN groupadd app && \
    useradd --create-home --gid app app

WORKDIR /app

COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app

RUN chown -R app:app /app

USER app

EXPOSE 8000

HEALTHCHECK \
    --interval=30s \
    --timeout=5s \
    --start-period=10s \
    --retries=3 \
    CMD python deployment/healthcheck.py || exit 1

CMD ["python", "-m", "deployment.startup"]