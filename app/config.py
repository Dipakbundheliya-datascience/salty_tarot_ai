import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

class Settings:
    """Simple configuration for FREE plan horoscope API"""
    
    # API Configuration
    APP_NAME: str = "Free Daily Horoscope API"
    VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Gemini API
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    
    # File Paths
    PROMPT_PATH: str = "app/horoscope_prompt.txt"
    
    # Rate Limiting (FREE plan limits)
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "5"))  # 5 requests per minute for free
    RATE_LIMIT_PERIOD: int = 60  # 1 minute
    
    # Zodiac Sign Date Ranges (month, day)
    ZODIAC_DATES = [
        ("Capricorn", 12, 22, 1, 19),    # Dec 22 - Jan 19
        ("Aquarius", 1, 20, 2, 18),      # Jan 20 - Feb 18  
        ("Pisces", 2, 19, 3, 20),        # Feb 19 - Mar 20
        ("Aries", 3, 21, 4, 19),         # Mar 21 - Apr 19
        ("Taurus", 4, 20, 5, 20),        # Apr 20 - May 20
        ("Gemini", 5, 21, 6, 20),        # May 21 - Jun 20
        ("Cancer", 6, 21, 7, 22),        # Jun 21 - Jul 22
        ("Leo", 7, 23, 8, 22),           # Jul 23 - Aug 22
        ("Virgo", 8, 23, 9, 22),         # Aug 23 - Sep 22
        ("Libra", 9, 23, 10, 22),        # Sep 23 - Oct 22
        ("Scorpio", 10, 23, 11, 21),     # Oct 23 - Nov 21
        ("Sagittarius", 11, 22, 12, 21)  # Nov 22 - Dec 21
    ]
    
    # Basic Zodiac Properties (for prompt context)
    ZODIAC_TRAITS = {
        "Aries": {
            "element": "Fire",
            "traits": ["energetic", "ambitious", "independent", "confident"],
            "focus_areas": ["career", "leadership", "new beginnings"]
        },
        "Taurus": {
            "element": "Earth", 
            "traits": ["reliable", "practical", "determined", "loyal"],
            "focus_areas": ["finances", "stability", "relationships"]
        },
        "Gemini": {
            "element": "Air",
            "traits": ["curious", "adaptable", "communicative", "witty"], 
            "focus_areas": ["communication", "learning", "social connections"]
        },
        "Cancer": {
            "element": "Water",
            "traits": ["nurturing", "intuitive", "emotional", "protective"],
            "focus_areas": ["family", "home", "emotions", "security"]
        },
        "Leo": {
            "element": "Fire",
            "traits": ["confident", "generous", "creative", "dramatic"],
            "focus_areas": ["creativity", "romance", "self-expression", "recognition"]
        },
        "Virgo": {
            "element": "Earth", 
            "traits": ["analytical", "practical", "helpful", "perfectionist"],
            "focus_areas": ["health", "work", "organization", "service"]
        },
        "Libra": {
            "element": "Air",
            "traits": ["diplomatic", "balanced", "social", "artistic"],
            "focus_areas": ["relationships", "harmony", "beauty", "justice"]
        },
        "Scorpio": {
            "element": "Water",
            "traits": ["intense", "passionate", "mysterious", "transformative"],
            "focus_areas": ["transformation", "intimacy", "power", "psychology"]
        },
        "Sagittarius": {
            "element": "Fire",
            "traits": ["adventurous", "optimistic", "philosophical", "free-spirited"],
            "focus_areas": ["travel", "education", "philosophy", "freedom"]
        },
        "Capricorn": {
            "element": "Earth",
            "traits": ["ambitious", "disciplined", "responsible", "practical"],
            "focus_areas": ["career", "goals", "authority", "structure"]
        },
        "Aquarius": {
            "element": "Air", 
            "traits": ["innovative", "independent", "humanitarian", "eccentric"],
            "focus_areas": ["friendships", "innovation", "social causes", "future"]
        },
        "Pisces": {
            "element": "Water",
            "traits": ["intuitive", "compassionate", "artistic", "spiritual"],
            "focus_areas": ["spirituality", "creativity", "compassion", "dreams"]
        }
    }
    
    def validate_config(self):
        """Validate required configuration"""
        if not self.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is required")

# Global settings instance
settings = Settings()

# Validate on import
try:
    settings.validate_config()
    print("✅ Configuration loaded successfully")
except ValueError as e:
    print(f"❌ Configuration Error: {e}")
    print("Please set GEMINI_API_KEY in your .env file")