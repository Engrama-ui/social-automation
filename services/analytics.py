from datetime import datetime, timedelta
from typing import List, Dict, Optional
from database import db
from models import SocialAccount, ScheduledPost, Engagement
from collections import defaultdict

class AnalyticsEngine:
    def __init__(self):
        self.cache = {}
        
    def get_account_analytics(self, account_id: int) -> Dict:
        """Ottieni le metriche principali per un account"""
        account = SocialAccount.query.get(account_id)
        if not account:
            raise ValueError("Account not found")
            
        return {
            "followers": account.followers_count,
            "engagement_rate": self._calculate_engagement_rate(account),
            "best_performing_post": self._get_best_performing_post(account),
            "weekly_growth": self._calculate_weekly_growth(account)
        }
        
    def get_post_analytics(self, post_id: int) -> Dict:
        """Analisi dettagliata per un singolo post"""
        post = ScheduledPost.query.get(post_id)
        if not post:
            raise ValueError("Post not found")
            
        return {
            "impressions": post.engagements.impressions,
            "engagement_rate": self._calculate_post_engagement_rate(post),
            "hashtag_performance": self._analyze_hashtag_performance(post),
            "sentiment_analysis": self._analyze_sentiment(post)
        }
        
    def generate_report(self, account_id: int, period: str = "30d") -> Dict:
        """Genera un report completo per un account"""
        account = SocialAccount.query.get(account_id)
        if not account:
            raise ValueError("Account not found")
            
        return {
            "summary": self.get_account_analytics(account_id),
            "top_posts": self._get_top_posts(account, period),
            "audience_insights": self._get_audience_insights(account),
            "recommendations": self._generate_recommendations(account)
        }
        
    def _calculate_engagement_rate(self, account: SocialAccount) -> float:
        """Calcola il tasso di engagement"""
        total_engagements = sum(
            post.engagements.likes + 
            post.engagements.comments + 
            post.engagements.shares
            for post in account.posts
        )
        
        if account.followers_count == 0:
            return 0
            
        return (total_engagements / account.followers_count) * 100
        
    def _get_best_performing_post(self, account: SocialAccount) -> Optional[Dict]:
        """Trova il post con le migliori prestazioni"""
        if not account.posts:
            return None
            
        best_post = max(
            account.posts, 
            key=lambda p: p.engagements.likes + p.engagements.comments + p.engagements.shares
        )
        
        return {
            "id": best_post.id,
            "content": best_post.content,
            "engagement": best_post.engagements.likes + best_post.engagements.comments + best_post.engagements.shares
        }
        
    def _calculate_weekly_growth(self, account: SocialAccount) -> Dict:
        """Calcola la crescita settimanale"""
        # Implementazione dettagliata omessa per brevità
        return {
            "followers": 0,
            "engagement": 0,
            "reach": 0
        }
        
    def _calculate_post_engagement_rate(self, post: ScheduledPost) -> float:
        """Calcola il tasso di engagement per un post"""
        if post.engagements.impressions == 0:
            return 0
            
        return (
            (post.engagements.likes + post.engagements.comments + post.engagements.shares) /
            post.engagements.impressions
        ) * 100
        
    def _analyze_hashtag_performance(self, post: ScheduledPost) -> Dict:
        """Analizza le prestazioni degli hashtag usati nel post"""
        hashtags = post.hashtags
        performance = {}
        
        for hashtag in hashtags:
            performance[hashtag.tag] = {
                "impressions": post.engagements.impressions,
                "engagement": post.engagements.likes + post.engagements.comments + post.engagements.shares
            }
            
        return performance
        
    def _analyze_sentiment(self, post: ScheduledPost) -> Dict:
        """Analisi del sentiment dei commenti"""
        # Implementazione dettagliata omessa per brevità
        return {
            "positive": 0,
            "neutral": 0,
            "negative": 0
        }
        
    def _get_top_posts(self, account: SocialAccount, period: str) -> List[Dict]:
        """Ottieni i migliori post per un determinato periodo"""
        # Implementazione dettagliata omessa per brevità
        return []
        
    def _get_audience_insights(self, account: SocialAccount) -> Dict:
        """Ottieni informazioni sul pubblico"""
        # Implementazione dettagliata omessa per brevità
        return {}
        
    def _generate_recommendations(self, account: SocialAccount) -> List[str]:
        """Genera raccomandazioni per migliorare le prestazioni"""
        # Implementazione dettagliata omessa per brevità
        return []