"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel

class InfoResponse(BaseModel):
    """Basic info response model"""
    app_name: str
    version: str
    description: str

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    service: str
    is_database_connected: str