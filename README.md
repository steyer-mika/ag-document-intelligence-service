# AG Document Intelligence Service

A Python-based service that processes scanned PDF documents and extracts structured data using OCR and computer vision technologies.

## Prerequisites

- Docker installed on your system
- Git (to clone the repository)

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/steyer-mika/ag-document-intelligence-service.git
   cd ag-document-intelligence-service
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
  "app_name": "Document Intelligence Service",
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
  "status": "ok",
  "service": "Document Intelligence Service",
  "is_database_connected": "connected"
}
```

### Jobs

#### Create Job

```
POST /jobs
```

Upload a PDF document to create a processing job.

**Request:**

- `file` (PDF) — The document to be processed.

**Response:**

```json
{
  "job_id": 123
}
```

#### Get Job Status

```
GET /jobs/{job_id}
```

Retrieve information about a specific job.

**Response:**

```json
{
  "id": 123,
  "status": "pending",
  "created_at": "2026-02-08T15:03:00.754629+00:00",
  "started_at": "2026-02-08T15:03:00.922156+00:00",
  "completed_at": "2026-02-08T15:04:06.098912+00:00",
  "error": null
}
```

#### Get Job Result

```
GET /jobs/{job_id}/{format}
```

Retrieve the extraction result for a completed job.

**Supported formats:** `json`, `csv`

**Response (JSON example):**

```json
{
  "job_id": 123,
  "total_pages": 6,
  "positions": [
    {
      "article_number": {
        "value": "01351062",
        "confidence": 96
      },
      "description": {
        "value": "CONDI.BALSAMI.BIANCO",
        "confidence": 89
      },
      "kvk": {
        "value": 8.99,
        "confidence": 92
      },
      "wgp": {
        "value": 5.805,
        "confidence": 54
      }
    }
  ]
}
```

**Response (CSV example):**

```csv
article_number,article_number_confidence,description,description_confidence,kvk,kvk_confidence,wgp,wgp_confidence
01351062,96.0,CONDI.BALSAMI.BIANCO,89.0,8.99,92.0,5.805,54.0
```

### Docs

```
GET /docs
```

Open in Browser for Swagger UI.

## Migrate for DEV

```bash
docker compose exec ag-document-intelligence-service-api alembic -c /app/alembic/alembic.ini revision --autogenerate -m "create jobs table"
docker compose exec ag-document-intelligence-service-api alembic -c /app/alembic/alembic.ini upgrade head
```
