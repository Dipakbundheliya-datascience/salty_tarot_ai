import asyncio
from google import genai
from app.config import settings
from datetime import datetime
from app.logger import logger

class GeminiClient:
    """Simple Gemini API client for FREE plan horoscopes"""
    
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.prompt_template = None
    
    def load_prompt(self) -> str:
        """Load horoscope prompt from text file"""
        try:
            with open(settings.PROMPT_PATH, 'r', encoding='utf-8') as file:
                self.prompt_template = file.read()
                logger.info("Horoscope prompt loaded successfully from file")
                return self.prompt_template
        except FileNotFoundError:
            # Fallback prompt if file doesn't exist
            logger.warning(f"Prompt file not found at {settings.PROMPT_PATH}, using fallback prompt")
            return """You are a professional astrologer. Generate a daily horoscope for {zodiac_sign}.
            
                        User Profile:
                        - Zodiac Sign: {zodiac_sign}
                        - Element: {element}
                        - Key Traits: {traits}
                        - Focus Areas: {focus_areas}
                        - Today's Date: {current_date}
                        - User Name: {user_name}

                        Generate a personalized, encouraging daily horoscope (2 paragraphs, 4-6 sentences each) that:
                        - Feels personal and relevant
                        - Addresses relationships, career, or personal growth
                        - Uses a warm, mystical tone
                        - Provides actionable advice
                        - Is written for American audience

                        Make it inspiring and positive while being specific to {zodiac_sign} traits.
                    """
    
    async def generate_horoscope(self, zodiac_sign: str, zodiac_traits: dict, user_name: str = None) -> str:
        """Generate horoscope using Gemini API"""
        logger.info(f"Generating horoscope for {zodiac_sign}, user: {user_name}")
        
        try:
            # Load prompt template
            if not self.prompt_template:
                self.load_prompt()
            
            # Get current date
            current_date = datetime.now().strftime("%B %d, %Y")
            
            # Prepare prompt data
            traits_str = ", ".join(zodiac_traits.get("traits", ["unique"]))
            focus_areas_str = ", ".join(zodiac_traits.get("focus_areas", ["general life"]))
            user_name_str = user_name if user_name else "dear friend"
            
            # Format the prompt
            formatted_prompt = self.prompt_template.format(
                zodiac_sign=zodiac_sign,
                element=zodiac_traits.get("element", "Unknown"),
                traits=traits_str,
                focus_areas=focus_areas_str,
                current_date=current_date,
                user_name=user_name_str
            )
            
            logger.info(f"Calling Gemini API with model: {settings.GEMINI_MODEL}")
            
            # Call Gemini API
            # response = self.client.models.generate_content(
            #     model=settings.GEMINI_MODEL,
            #     contents=[formatted_prompt]
            # )

            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.models.generate_content(
                    model=settings.GEMINI_MODEL,
                    contents=[formatted_prompt]
                )
            )
            
            horoscope_text = response.text.strip()
            logger.info(f"Gemini API response successful, generated {len(horoscope_text)} characters")
            
            # Return generated horoscope
            return horoscope_text
            
        except Exception as e:
            # Log the specific error
            logger.error(f"Gemini API error for {zodiac_sign}: {str(e)}")
            
            # Simple error fallback
            fallback_message = f"The stars are a bit cloudy today for {zodiac_sign}. Try again in a moment, and the cosmic energies will align for your personalized reading!"
            logger.info(f"Returning fallback message for {zodiac_sign}")
            return fallback_message

# Global client instance
gemini_client = GeminiClient()