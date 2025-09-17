from app.models import HoroscopeRequest, HoroscopeResponse
from app.zodiac_service import zodiac_service
from app.gemini_client import gemini_client

class HoroscopeService:
    """Main service for FREE plan horoscope generation"""
    
    def generate_daily_horoscope(self, request: HoroscopeRequest) -> HoroscopeResponse:
        """Generate complete horoscope response"""
        try:
            # Step 1: Validate birth date
            is_valid, error_msg = zodiac_service.validate_birth_date(request.birth_date)
            if not is_valid:
                raise ValueError(error_msg)
            
            # Step 2: Calculate zodiac sign
            zodiac_sign = zodiac_service.calculate_zodiac_sign(request.birth_date)
            
            # Step 3: Get zodiac traits for better context
            zodiac_traits = zodiac_service.get_zodiac_traits(zodiac_sign)
            
            # Step 4: Generate horoscope using Gemini
            horoscope_text = gemini_client.generate_horoscope(
                zodiac_sign=zodiac_sign,
                zodiac_traits=zodiac_traits,
                user_name=request.user_name
            )
            
            # Step 5: Create ultra simple response (just horoscope text)
            response = HoroscopeResponse(
                horoscope=horoscope_text
            )
            
            return response
            
        except ValueError as e:
            # Validation errors (bad date, etc.)
            raise e
        except Exception as e:
            # General errors (API failure, etc.)
            raise Exception(f"Unable to generate horoscope: {str(e)}")

# Global service instance
horoscope_service = HoroscopeService()