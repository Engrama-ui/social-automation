from datetime import datetime
from typing import List, Optional
from database import db
from models import Engagement, SocialAccount
from textblob import TextBlob

class EngagementTracker:
    def __init__(self):
        self.active_monitors = {}
        
    def track_comments(self, post_id: int):
        # Implementation for tracking comments
        pass
        
    def track_mentions(self, account_id: int):
        # Implementation for tracking mentions
        pass
        
    def get_engagement_metrics(self, post_id: int) -> Engagement:
        return Engagement.query.get(post_id)
        
    def analyze_sentiment(self, text: str) -> float:
        analysis = TextBlob(text)
        return analysis.sentiment.polarity
        
    def get_recent_engagements(
        self,
        account_id: int,
        limit: int = 100
    ) -> List[Engagement]:
        return Engagement.query.filter_by(account_id=account_id)\
            .order_by(Engagement.timestamp.desc())\
            .limit(limit)\
            .all()
            
    def get_engagement_summary(self, account_id: int) -> dict:
        account = SocialAccount.query.get(account_id)
        if not account:
            raise ValueError("Account not found")
            
        return {
            "total_likes": sum(e.likes for e in account.engagements),
            "total_comments": sum(e.comments for e in account.engagements),
            "total_shares": sum(e.shares for e in account.engagements),
            "average_sentiment": self._calculate_average_sentiment(account)
        }
        
    def _calculate_average_sentiment(self, account: SocialAccount) -> float:
        sentiments = [
            self.analyze_sentiment(c.text)
            for e in account.engagements
            for c in e.comments
        ]
        return sum(sentiments) / len(sentiments) if sentiments else 0