# ─────────────────────────────────────────────────────────────
#  VayuBus Backend — Dockerfile
#  Python FastAPI on port 8000
# ─────────────────────────────────────────────────────────────
FROM python:3.12-slim

LABEL app="vayubus-backend"
LABEL version="1.0.0"

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Non-root user
RUN addgroup --system appgroup && adduser --system --group appgroup
RUN chown -R appgroup:appgroup /app
USER appgroup

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
