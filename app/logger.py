import logging
import sys
from datetime import datetime
import os

def setup_logging():
    """Setup simple but effective logging for the horoscope API"""
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Configure logging format
    log_format = "%(asctime)s | %(levelname)-8s | %(name)-15s | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt=date_format,
        handlers=[
            # Console output (for development)
            logging.StreamHandler(sys.stdout),
            # File output (for production)
            logging.FileHandler(
                f"logs/horoscope_api_{datetime.now().strftime('%Y%m%d')}.log",
                encoding='utf-8'
            )
        ]
    )
    
    # Set specific log levels for different components
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)  # Reduce uvicorn noise
    logging.getLogger("httpx").setLevel(logging.WARNING)  # Reduce HTTP client noise
    
    return logging.getLogger("horoscope_api")

# Global logger instance
logger = setup_logging()