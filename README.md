# AG Document Intelligence Service

A Python-based service that processes scanned PDF documents and extracts structured data using OCR and computer vision technologies.

## Overview

This service automatically processes PDF documents containing product articles and extracts key information into a structured CSV format. It uses Optical Character Recognition (OCR) to read text from scanned documents and intelligently parses the content to identify specific data fields.

## Features

- **PDF Processing**: Accepts scanned PDF documents as input
- **Data Extraction**: Extracts the following fields per article:
  - Article Name (Artikelname)
  - KVK (Customer Unit of Measure)
  - WGP (Product Group)
  - Article Number (Artikelnummer)
- **CSV Export**: Outputs structured data in CSV format
- **OCR/Computer Vision**: Advanced text recognition from scanned documents
- **Error Handling**: Robust error handling for illegible or problematic areas
- **REST API**: FastAPI-based REST API for easy integration
- **Confidence Scores**: Returns confidence metrics for extracted data
- **Docker Support**: Fully containerized deployment

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
