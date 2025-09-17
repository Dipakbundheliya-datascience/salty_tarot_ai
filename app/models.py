from pydantic import BaseModel
from typing import Optional

class HoroscopeRequest(BaseModel):
    """Simple request for free horoscope"""
    birth_date: str  # Format: "1990-01-15" 
    user_name: str

class HoroscopeResponse(BaseModel):
    """Ultra simple response - just the horoscope text"""
    horoscope: str

class ErrorResponse(BaseModel):
    """Simple error response"""
    error: str
    message: str

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str