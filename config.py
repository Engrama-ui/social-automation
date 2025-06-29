from dotenv import load_dotenv
import os

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Recupera le variabili d'ambiente
FACEBOOK_APP_ID = os.getenv("FACEBOOK_APP_ID")
FACEBOOK_APP_SECRET = os.getenv("FACEBOOK_APP_SECRET")

class Settings:
    MEDIA_UPLOAD_DIR = os.environ.get("MEDIA_UPLOAD_DIR", "media_uploads")

settings = Settings()
