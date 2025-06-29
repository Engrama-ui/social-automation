import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from database import SessionLocal
from models import Hashtag, PostHashtag
from config import settings

class HashtagOptimizer:
    def __init__(self):
        self.api_key = settings.HASHTAG_API_KEY
        
    def research_hashtag(self, keyword: str) -> Dict:
        """Ricerca dati su un hashtag specifico"""
        try:
            response = requests.get(
                f"https://api.hashtagservice.com/v1/research?keyword={keyword}",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            return response.json()
        except Exception as e:
            raise Exception(f"Hashtag research failed: {str(e)}")
            
    def track_performance(self, hashtag_id: int) -> Dict:
        """Traccia le prestazioni di un hashtag nel tempo"""
        hashtag = Hashtag.query.get(hashtag_id)
        if not hashtag:
            raise ValueError("Hashtag not found")
            
        posts = PostHashtag.query.filter_by(hashtag_id=hashtag_id).all()
        engagement = sum(post.post.engagements.likes for post in posts)
        
        return {
            "hashtag": hashtag.tag,
            "total_posts": len(posts),
            "total_engagement": engagement,
            "average_engagement": engagement / len(posts) if posts else 0
        }
        
    def get_suggestions(self, content: str, n: int = 5) -> List[str]:
        """Genera suggerimenti hashtag basati sul contenuto"""
        keywords = self._extract_keywords(content)
        suggestions = []
        
        for keyword in keywords:
            data = self.research_hashtag(keyword)
            suggestions.extend(data.get("related_hashtags", []))
            
        return sorted(suggestions, key=lambda x: x["popularity"], reverse=True)[:n]
        
    def get_trending(self, platform: str = "all") -> List[Dict]:
        """Ottieni hashtag trend in tempo reale"""
        try:
            response = requests.get(
                f"https://api.hashtagservice.com/v1/trending?platform={platform}",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            return response.json().get("trends", [])
        except Exception as e:
            raise Exception(f"Failed to get trends: {str(e)}")
            
    def _extract_keywords(self, text: str) -> List[str]:
        """Estrazione parole chiave dal testo (implementazione semplificata)"""
        # Implementazione reale userebbe NLP
        return list(set(word.lower() for word in text.split() if word.startswith("#") and len(word) > 1))