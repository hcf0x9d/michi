import os
from dotenv import load_dotenv
load_dotenv()

RESOURCE = "https://resources.fukura.design/mission-driven-guide-to-digital-strategy"
BOOKING_LINK = "https://calendly.com/jason-fukura/introduction-call"
NAV_LINKS = [
    {"label": "Home", "endpoint": "public.home"},
    {"label": "Services", "endpoint": "public.services"},
    # {"label": "Resources", "endpoint": "public.resources"},
    {"label": "About", "endpoint": "public.about"},
    # {"label": "Contact", "endpoint": "public.contact"},
]



SOCIAL_LINKS = [
    {"label": "LinkedIn", "icon": "linkedin", "url": "https://www.linkedin.com/in/jason-fukura"},
    {"label": "Instagram", "icon": "instagram", "url": "https://www.instagram.com/jason.fukura.design"},
]

# Basic config (can be expanded)
ENVIRONMENT = os.getenv("FLASK_ENV")
GTM_ID = os.getenv("GTM_ID")
SECRET_KEY = os.getenv("SECRET_KEY")
HYGRAPH_API_URL = os.getenv("HYGRAPH_API_URL")
