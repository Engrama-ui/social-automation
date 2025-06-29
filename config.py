import os

class Settings:
    MEDIA_UPLOAD_DIR = os.environ.get("MEDIA_UPLOAD_DIR", "media_uploads")

settings = Settings()
