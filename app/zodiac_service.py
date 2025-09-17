from datetime import datetime
from app.config import settings
from app.logger import logger

class ZodiacService:
    """Simple zodiac sign calculator for FREE plan"""
    
    def calculate_zodiac_sign(self, birth_date_str: str) -> str:
        """Convert birth date string to zodiac sign"""
        try:
            # Parse date string (format: "1990-01-15")
            birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
            month = birth_date.month
            day = birth_date.day
            
            # Check each zodiac sign range
            for sign_info in settings.ZODIAC_DATES:
                sign_name = sign_info[0]
                
                if sign_name == "Capricorn":
                    # Special case: Dec 22 - Jan 19 (crosses year boundary)
                    if (month == 12 and day >= 22) or (month == 1 and day <= 19):
                        logger.info(f"Calculated zodiac sign: {sign_name} for {birth_date_str}")
                        return sign_name
                else:
                    start_month = sign_info[1]
                    start_day = sign_info[2]
                    end_month = sign_info[3]
                    end_day = sign_info[4]
                    
                    # Check if date falls in this sign's range
                    if (month == start_month and day >= start_day) or \
                       (month == end_month and day <= end_day):
                        logger.info(f"Calculated zodiac sign: {sign_name} for {birth_date_str}")
                        return sign_name
            
            # Fallback (shouldn't happen)
            logger.warning(f"Could not determine zodiac sign for {birth_date_str}, defaulting to Capricorn")
            return "Capricorn"
            
        except ValueError as e:
            logger.error(f"Invalid birth date format: {birth_date_str}")
            raise ValueError("Invalid birth date format. Use YYYY-MM-DD")
    
    def get_zodiac_traits(self, zodiac_sign: str) -> dict:
        """Get basic traits for a zodiac sign"""
        return settings.ZODIAC_TRAITS.get(zodiac_sign, {
            "element": "Unknown",
            "traits": ["unique"],
            "focus_areas": ["general life"]
        })
    
    def validate_birth_date(self, birth_date_str: str) -> tuple[bool, str]:
        """Simple validation for birth date"""
        try:
            birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
            
            # Check if date is not in future
            if birth_date.date() > datetime.now().date():
                return False, "Birth date cannot be in the future"
            
            # Check reasonable year range
            if birth_date.year < 1900:
                return False, "Birth date must be after 1900"
            
            return True, ""
            
        except ValueError:
            return False, "Invalid date format. Use YYYY-MM-DD"

# Global service instance
zodiac_service = ZodiacService()