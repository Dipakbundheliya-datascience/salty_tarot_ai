from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uvicorn

from app.config import settings
from app.models import HoroscopeRequest, HoroscopeResponse, ErrorResponse, HealthResponse
from app.horoscope_service import horoscope_service

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Free daily horoscope predictions based on date of birth using AI"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Simple health check"""
    return HealthResponse(
        status="healthy",
        version=settings.VERSION
    )

# Main horoscope endpoint (FREE plan)
@app.post("/horoscope", response_model=HoroscopeResponse)
async def generate_horoscope(horoscope_request: HoroscopeRequest):
    """Generate daily horoscope for FREE users"""
    try:
        # Generate horoscope using the service
        response = horoscope_service.generate_daily_horoscope(horoscope_request)
        return response
        
    except ValueError as e:
        # Validation errors (bad date format, future date, etc.)
        raise HTTPException(
            status_code=400,
            detail=f"Invalid request: {str(e)}"
        )
    except Exception as e:
        # General errors (API failure, etc.)
        raise HTTPException(
            status_code=500,
            detail=f"Unable to generate horoscope: {str(e)}"
        )

# Root endpoint
@app.get("/")
async def root():
    """API information"""
    return {
        "message": "Free Daily Horoscope API",
        "version": settings.VERSION,
        "endpoints": {
            "generate_horoscope": "POST /horoscope",
            "health": "GET /health"
        },
        "plan": "FREE"
    }

# Run the app
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )