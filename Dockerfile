# Stage 1: Build dependencies
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y gcc build-essential && rm -rf /var/lib/apt/lists/*

# Create a virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Stage 2: Final image
FROM python:3.12-slim

# Create a non-root user
RUN useradd -ms /bin/bash fastapiuser

# Set up virtual environment
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy virtual environment and application code from builder
COPY --from=builder /opt/venv /opt/venv
WORKDIR /home/fastapiuser/app
COPY . .

# Set permissions
RUN chown -R fastapiuser:fastapiuser /home/fastapiuser

# Switch to non-root user
USER fastapiuser

# Expose application port
EXPOSE 8000

# Start FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]