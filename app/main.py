import time
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware 

from app.logger import logger
from app.config import settings
from app.horoscope_service import horoscope_service
from app.models import HoroscopeRequest, HoroscopeResponse, HealthResponse

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
    logger.info("Health check requested")
    return HealthResponse(
        status="healthy",
        version=settings.VERSION
    )

# Main horoscope endpoint (FREE plan)
@app.post("/horoscope", response_model=HoroscopeResponse)
async def generate_horoscope(horoscope_request: HoroscopeRequest):
    """Generate daily horoscope for FREE users"""
    request_start_time = time.time() 
    logger.info(f"Horoscope request: birth_date={horoscope_request.birth_date}, user_name={horoscope_request.user_name}")
    
    try:
        # Generate horoscope using the service
        response = await horoscope_service.generate_daily_horoscope(horoscope_request)
       
        request_end_time = time.time()
        total_time = round(request_end_time - request_start_time, 2)  # ← ADD THIS LINE
        logger.info(f"🎉 Request completed in {total_time}s for user: {horoscope_request.user_name} | Horoscope: {response.horoscope[:50]}...")

        return response
        
    except ValueError as e:
        # Validation errors (bad date format, future date, etc.)
        logger.warning(f"Validation error: {str(e)} for birth_date={horoscope_request.birth_date}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid request: {str(e)}"
        )
    except Exception as e:
        # General errors (API failure, etc.)
        logger.error(f"Unexpected error generating horoscope: {str(e)} for birth_date={horoscope_request.birth_date}")
        raise HTTPException(
            status_code=500,
            detail=f"Unable to generate horoscope: {str(e)}"
        )

# Root endpoint
@app.get("/")
async def root():
    """API information"""
    logger.info("API info requested")
    return {
        "message": "Free Daily Horoscope API",
        "version": settings.VERSION,
        "endpoints": {
            "generate_horoscope": "POST /horoscope",
            "health": "GET /health"
        },
        "plan": "FREE"
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    """Log application startup"""
    logger.info(f"🌟 {settings.APP_NAME} v{settings.VERSION} starting up")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"Gemini model: {settings.GEMINI_MODEL}")

# Shutdown event  
@app.on_event("shutdown")
async def shutdown_event():
    """Log application shutdown"""
    logger.info("🛑 Horoscope API shutting down")

# Run the app
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )