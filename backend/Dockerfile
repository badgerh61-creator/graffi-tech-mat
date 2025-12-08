FROM python:3.11-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1

# ---------------------------------------------------
# Install system dependencies
# ---------------------------------------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    python3-dev \
    ffmpeg \
    curl \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# ---------------------------------------------------
# Install MinIO Client (mc)
# ---------------------------------------------------
RUN curl -sSL https://dl.min.io/client/mc/release/linux-amd64/mc \
    -o /usr/local/bin/mc && chmod +x /usr/local/bin/mc

# ---------------------------------------------------
# Install Python dependencies
# ---------------------------------------------------
COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# ---------------------------------------------------
# Copy backend source
# ---------------------------------------------------
COPY . /app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
