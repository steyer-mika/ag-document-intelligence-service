"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field

class InfoResponse(BaseModel):
    """Basic info response model"""
    app_name: str
    version: str
    description: str

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    service: str