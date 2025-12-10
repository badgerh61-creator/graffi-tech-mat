# ===========================
# Backend: Multi-stage build
# ===========================

FROM python:3.11-slim AS builder

WORKDIR /app

# Install build tools for required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libjpeg-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Build dependency wheels
RUN pip install --upgrade pip && pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

# Copy backend source
COPY app ./app


# ===========================
# Runtime container
# ===========================

FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*

# Copy backend source
COPY --from=builder /app/app ./app

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

