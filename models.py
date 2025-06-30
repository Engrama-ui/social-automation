from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime)

class SocialAccount(Base):
    __tablename__ = "social_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    platform = Column(String)
    access_token = Column(String)
    refresh_token = Column(String)
    last_sync = Column(DateTime)
    
    user = relationship("User", back_populates="accounts")

class ScheduledPost(Base):
    __tablename__ = "scheduled_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("social_accounts.id"))
    content = Column(String)
    scheduled_time = Column(DateTime)
    status = Column(String)
    
    account = relationship("SocialAccount", back_populates="posts")
    engagements = relationship("Engagement", back_populates="post")
    hashtags = relationship("PostHashtag", back_populates="post")

class Engagement(Base):
    __tablename__ = "engagements"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("scheduled_posts.id"))
    likes = Column(Integer)
    comments = Column(Integer)
    shares = Column(Integer)
    sentiment_score = Column(Float)
    last_updated = Column(DateTime)
    
    post = relationship("ScheduledPost", back_populates="engagements")

class Hashtag(Base):
    __tablename__ = "hashtags"
    
    id = Column(Integer, primary_key=True, index=True)
    tag = Column(String, unique=True)
    popularity_score = Column(Float)
    last_analyzed = Column(DateTime)
    
    posts = relationship("PostHashtag", back_populates="hashtag")

class PostHashtag(Base):
    __tablename__ = "post_hashtags"
    
    post_id = Column(Integer, ForeignKey("scheduled_posts.id"), primary_key=True)
    hashtag_id = Column(Integer, ForeignKey("hashtags.id"), primary_key=True)
    
    post = relationship("ScheduledPost", back_populates="hashtags")
    hashtag = relationship("Hashtag", back_populates="posts")

class ContentTemplate(Base):
    __tablename__ = "content_templates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    content = Column(String)
    variables = Column(JSON)

class MediaFile(Base):
    __tablename__ = "media_files"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    filename = Column(String)
    filepath = Column(String)
    mime_type = Column(String)
    created_at = Column(DateTime)

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String)
    notification_type = Column(String)
    read = Column(Boolean, default=False)
    timestamp = Column(DateTime)

class SystemStatus(Base):
    __tablename__ = "system_status"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime)
    services_status = Column(JSON)
    cpu_usage = Column(Float)
    memory_usage = Column(Float)

class ContentTemplate(Base):
    __tablename__ = "content_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    content = Column(String, nullable=False)
    variables = Column(JSON, default={})
    # Se vuoi collegare il template a un utente, decommenta la riga seguente:
    # user_id = Column(Integer, ForeignKey("users.id"))
    # user = relationship("User")

class MediaFile(Base):
    __tablename__ = "media_files"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    mime_type = Column(String, nullable=False)
    created_at = Column(DateTime)
    # user = relationship("User")  # opzionale, se vuoi la relazione

class UserPreferences(Base):
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    timezone = Column(String, default="Europe/Rome")
    language = Column(String, default="it")
    email_notifications = Column(Boolean, default=True)
    engagement_alerts = Column(Boolean, default=True)
    weekly_reports = Column(Boolean, default=False)
    optimization_tips = Column(Boolean, default=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    
    user = relationship("User", back_populates="preferences")

# Add relationships
User.accounts = relationship("SocialAccount", back_populates="user")
User.preferences = relationship("UserPreferences", back_populates="user", uselist=False)
SocialAccount.posts = relationship("ScheduledPost", back_populates="account")

# Espone ContentTemplate per l'import nei servizi
__all__ = [
    'User', 'SocialAccount', 'ScheduledPost', 'Engagement', 'Hashtag', 'PostHashtag', 'Notification', 'SystemStatus', 'ContentTemplate', 'MediaFile'
]