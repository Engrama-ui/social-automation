import os
from typing import List, Optional
from datetime import datetime
from database import SessionLocal
from models import MediaFile
from config import settings

class MediaManager:
    def __init__(self):
        self.upload_dir = settings.MEDIA_UPLOAD_DIR
        os.makedirs(self.upload_dir, exist_ok=True)
        
    def save_media(self, file, user_id: int) -> MediaFile:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{user_id}_{timestamp}_{file.filename}"
        filepath = os.path.join(self.upload_dir, filename)
        
        with open(filepath, "wb") as buffer:
            buffer.write(file.file.read())
            
        media = MediaFile(
            user_id=user_id,
            filename=filename,
            filepath=filepath,
            mime_type=file.content_type
        )
        
        db.session.add(media)
        db.session.commit()
        return media
        
    def get_media(self, media_id: int) -> Optional[MediaFile]:
        return MediaFile.query.get(media_id)
        
    def list_user_media(self, user_id: int) -> List[MediaFile]:
        return MediaFile.query.filter_by(user_id=user_id).all()
        
    def delete_media(self, media_id: int) -> bool:
        media = MediaFile.query.get(media_id)
        if media:
            try:
                os.remove(media.filepath)
            except FileNotFoundError:
                pass
            db.session.delete(media)
            db.session.commit()
            return True
        return False