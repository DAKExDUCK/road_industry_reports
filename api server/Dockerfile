FROM python:3.13-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install build dependencies required for some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
		build-essential \
		gcc \
		libpq-dev \
	&& rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN python -m pip install --upgrade pip
# Install into an isolated prefix so we can copy only installed packages to final image
RUN pip install --prefix=/install -r requirements.txt


FROM python:3.13-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Minimal runtime dependencies (libpq for postgres client libraries)
RUN apt-get update && apt-get install -y --no-install-recommends \
		libpq5 \
	&& rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY . /app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
