# Multi-stage Dockerfile for Margadarsaka deployment to Google Cloud Platform
# Optimized with UV package manager and Doppler secrets management

FROM python:3.12-slim as builder

# Install system dependencies for building
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock* ./
COPY src/ ./src/

# Install dependencies
RUN uv sync --frozen

# Production stage
FROM python:3.12-slim as production

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Doppler CLI for secrets management
RUN curl -Ls https://cli.doppler.com/install.sh | sh

# Install uv in production
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Copy installed dependencies and application from builder
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src
COPY --from=builder /app/pyproject.toml /app/pyproject.toml

# Create necessary directories
RUN mkdir -p /app/data /app/logs && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Health check for container orchestration
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

# Environment variables
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"
ENV PORT=8000

# Expose ports (8000 for API, 8501 for Streamlit)
EXPOSE 8000 8501

# Default command - uses Doppler if DOPPLER_TOKEN is provided, falls back to env vars
CMD ["sh", "-c", "if [ -n \"$DOPPLER_TOKEN\" ]; then doppler run --token=\"$DOPPLER_TOKEN\" -- uv run margadarsaka; else uv run margadarsaka; fi"]

# Alternative commands for different deployment scenarios:
# API only: CMD ["uv", "run", "--frozen", "uvicorn", "src.margadarsaka.api:app", "--host", "0.0.0.0", "--port", "${PORT:-8000}"]
# UI only: CMD ["uv", "run", "streamlit", "run", "src/margadarsaka/ui.py", "--server.port=${PORT:-8501}"]
# Development: CMD ["uv", "run", "margadarsaka"]