# AG Document Intelligence Service

A Python-based service that processes scanned PDF documents and extracts structured data using OCR and computer vision technologies.

## Prerequisites

- Docker installed on your system
- Git (to clone the repository)

## Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Configure environment variables**

   ```bash
   cp .env.example .env
   ```

   Edit the `.env` file with your specific configuration if needed.

3. **Start the service**
   ```bash
   docker compose up -d
   ```

The service will start and be accessible at `http://localhost:8000` (or the port specified in your configuration).

## API Reference

### Root Endpoint

```
GET /
```

Returns the service name and version information.

**Response:**

```json
{
  "name": "Document Intelligence Service",
  "version": "1.0.0",
  "description": "Extracts structured data from documents using OCR technologies."
}
```

### Health Check

```
GET /health
```

Health check endpoint to verify service status.

**Response:**

```json
{
  "status": "healthy"
}
```

### Docs

```
GET /docs
```

Open in Browser for Swagger UI.

## Migrate for DEV

(Note: Somehow it only works in Powershell and not in bash?)

docker compose exec ag-document-intelligence-service-api alembic -c /app/alembic/alembic.ini revision --autogenerate -m "create jobs table"
docker compose exec ag-document-intelligence-service-api alembic -c /app/alembic/alembic.ini upgrade head
