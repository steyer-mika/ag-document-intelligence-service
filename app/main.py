from fastapi import FastAPI

from app.api import routes
from app.config.settings import settings

app = FastAPI(
    title="Document Intelligence Service",
    description="Extracts structured data from documents using OCR technologies.",
    version="1.0.0",
)

app.include_router(routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.API_HOST,
        port=settings.API_PORT,
    )