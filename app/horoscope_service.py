from app.models import HoroscopeRequest, HoroscopeResponse
from app.zodiac_service import zodiac_service
from app.gemini_client import gemini_client
from app.logger import logger

class HoroscopeService:
    """Main service for FREE plan horoscope generation"""
    
    async def generate_daily_horoscope(self, request: HoroscopeRequest) -> HoroscopeResponse:
        """Generate complete horoscope response"""
        logger.info(f"Starting horoscope generation for birth_date: {request.birth_date}")
        
        try:
            # Step 1: Validate birth date
            is_valid, error_msg = zodiac_service.validate_birth_date(request.birth_date)
            if not is_valid:
                logger.warning(f"Birth date validation failed: {error_msg}")
                raise ValueError(error_msg)
            
            # Step 2: Calculate zodiac sign
            zodiac_sign = zodiac_service.calculate_zodiac_sign(request.birth_date)
            
            # Step 3: Get zodiac traits for better context
            zodiac_traits = zodiac_service.get_zodiac_traits(zodiac_sign)
            logger.info(f"Retrieved traits for {zodiac_sign}: {zodiac_traits.get('element')} element")
            
            # Step 4: Generate horoscope using Gemini
            horoscope_text = await gemini_client.generate_horoscope(
                zodiac_sign=zodiac_sign,
                zodiac_traits=zodiac_traits,
                user_name=request.user_name
            )
            
            # Step 5: Create ultra simple response (just horoscope text)
            response = HoroscopeResponse(
                horoscope=horoscope_text,
                zodiac_sign=zodiac_sign
            )
            
            logger.info(f"Horoscope generation completed successfully for {zodiac_sign}")
            return response
            
        except ValueError as e:
            # Validation errors (bad date, etc.)
            logger.error(f"Validation error in horoscope service: {str(e)}")
            raise e
        except Exception as e:
            # General errors (API failure, etc.)
            logger.error(f"Unexpected error in horoscope service: {str(e)}")
            raise Exception(f"Unable to generate horoscope: {str(e)}")

# Global service instance
horoscope_service = HoroscopeService()