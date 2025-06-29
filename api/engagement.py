from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from datetime import datetime
from pydantic import BaseModel, Field
from services.engagement import EngagementTracker
from auth import get_current_user

router = APIRouter(
    prefix="/engagement", 
    tags=["💬 Engagement e Interazioni"],
    responses={
        404: {"description": "Dati engagement non trovati"},
        400: {"description": "Parametri non validi"},
        401: {"description": "Non autorizzato"}
    }
)

class EngagementResponse(BaseModel):
    post_id: int = Field(..., description="🆔 ID del post")
    likes: int = Field(..., description="❤️ Numero di like")
    comments: int = Field(..., description="💬 Numero di commenti")
    shares: int = Field(..., description="🔄 Numero di condivisioni")
    sentiment_score: float = Field(..., description="😊 Punteggio sentiment (-1 a +1)")
    timestamp: datetime = Field(..., description="⏰ Timestamp dei dati")
    
    class Config:
        json_schema_extra = {
            "example": {
                "post_id": 123,
                "likes": 245,
                "comments": 32,
                "shares": 18,
                "sentiment_score": 0.75,
                "timestamp": "2024-01-15T14:30:00Z"
            }
        }

class EngagementSummary(BaseModel):
    total_likes: int = Field(..., description="❤️ Totale like raccolti")
    total_comments: int = Field(..., description="💬 Totale commenti ricevuti")
    total_shares: int = Field(..., description="🔄 Totale condivisioni")
    average_sentiment: float = Field(..., description="😊 Sentiment medio (-1 a +1)")

@router.get(
    "/post/{post_id}", 
    response_model=EngagementResponse,
    summary="📊 Engagement di un post specifico",
    description="""
    ## 💬 Analisi dettagliata dell'engagement di un post
    
    Ottieni metriche complete di engagement:
    - **❤️ Like**: Apprezzamento del contenuto
    - **💬 Commenti**: Livello di discussione generata
    - **🔄 Condivisioni**: Viralità del contenuto
    - **😊 Sentiment**: Analisi emotiva dei commenti
    
    ### 📈 Come interpretare i dati:
    - **Alto engagement**: Contenuto risonante con audience
    - **Sentiment positivo**: Reazioni favorevoli (+0.5 a +1.0)
    - **Molti commenti**: Contenuto che stimola discussione
    - **Molte condivisioni**: Contenuto viral-worthy
    
    ### 💡 Insights strategici:
    - **Sentiment negativo**: Analizza feedback per migliorare
    - **Alto share/like ratio**: Contenuto molto rilevante
    - **Pochi commenti ma molti like**: Contenuto passivo
    - **Molti commenti**: Controlla qualità discussione
    """,
    responses={
        200: {
            "description": "✅ Dati engagement recuperati",
            "content": {
                "application/json": {
                    "example": {
                        "post_id": 123,
                        "likes": 245,
                        "comments": 32,
                        "shares": 18,
                        "sentiment_score": 0.75,
                        "timestamp": "2024-01-15T14:30:00Z"
                    }
                }
            }
        }
    }
)
async def get_post_engagement(
    post_id: int,
    user = Depends(get_current_user)
):
    """
    Recupera dati di engagement dettagliati per un post specifico.
    
    Utile per:
    - Analisi performance singoli post
    - Identificazione contenuti top performer  
    - Monitoraggio sentiment audience
    - Ottimizzazione strategia contenuti
    """
    tracker = EngagementTracker()
    engagement = tracker.get_engagement_metrics(post_id)
    if not engagement:
        raise HTTPException(status_code=404, detail="❌ Dati engagement non trovati per questo post")
    return engagement

@router.get(
    "/account/{account_id}/recent", 
    response_model=List[EngagementResponse],
    summary="📈 Engagement recenti dell'account",
    description="""
    ## 📊 Cronologia engagement per account
    
    Visualizza engagement recenti per analisi trend:
    - **⏰ Dati ordinati** per data (più recenti primi)
    - **📊 Metriche complete** per ogni post
    - **🎯 Limite configurabile** per performance
    - **📈 Identificazione pattern** temporali
    
    ### 💡 Analisi consigliata:
    - **Trend temporali**: Giorni/orari migliori per engagement
    - **Tipo contenuti**: Quali generano più interazioni
    - **Sentiment evolution**: Cambiamenti percezione brand
    - **Performance decay**: Degradazione engagement nel tempo
    
    ### 🎯 Azioni suggerite:
    - **Top performers**: Replica strategia contenuti migliori
    - **Sentiment negativo**: Intervieni rapidamente su problemi
    - **Calo engagement**: Varia strategia contenuti
    - **Pattern orari**: Ottimizza scheduling post
    """,
    responses={
        200: {
            "description": "✅ Lista engagement recuperata",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "post_id": 125,
                            "likes": 89,
                            "comments": 12,
                            "shares": 5,
                            "sentiment_score": 0.65,
                            "timestamp": "2024-01-15T14:30:00Z"
                        },
                        {
                            "post_id": 124,
                            "likes": 156,
                            "comments": 23,
                            "shares": 11,
                            "sentiment_score": 0.82,
                            "timestamp": "2024-01-14T10:15:00Z"
                        }
                    ]
                }
            }
        }
    }
)
async def get_recent_engagements(
    account_id: int,
    limit: int = Query(100, description="🔢 Numero massimo di risultati", ge=1, le=500),
    user = Depends(get_current_user)
):
    """
    Recupera i dati di engagement più recenti per un account.
    
    Perfetto per:
    - Dashboard engagement overview
    - Analisi trend recenti
    - Monitoraggio performance quotidiana
    - Report settimanali/mensili
    """
    tracker = EngagementTracker()
    return tracker.get_recent_engagements(account_id, limit)

@router.get(
    "/account/{account_id}/summary", 
    response_model=EngagementSummary,
    summary="📊 Riepilogo engagement account",
    description="""
    ## 📈 Panoramica completa engagement dell'account
    
    Ottieni statistiche aggregate di tutti i post:
    - **❤️ Total Likes**: Somma di tutti i like ricevuti
    - **💬 Total Comments**: Tutti i commenti generati
    - **🔄 Total Shares**: Condivisioni totali dei contenuti
    - **😊 Average Sentiment**: Sentiment medio delle interazioni
    
    ### 📊 Benchmark di riferimento:
    - **Sentiment > 0.6**: Percezione molto positiva del brand
    - **Sentiment 0.3-0.6**: Percezione neutra/positiva
    - **Sentiment < 0.3**: Richiede attenzione e miglioramenti
    
    ### 💡 Insights strategici:
    - **Alto numero interazioni**: Brand con buon engagement
    - **Sentiment positivo stabile**: Strategia contenuti efficace
    - **Share/Like ratio alto**: Contenuti molto rilevanti
    - **Commenti abbondanti**: Community attiva ed engaged
    
    ### 🎯 Azioni raccomandate:
    - **Sentiment in calo**: Rivedi strategia messaging
    - **Poche interazioni**: Aumenta call-to-action
    - **Molti like, pochi commenti**: Crea contenuti più discussione-friendly
    - **Performance costante**: Mantieni e scala strategia attuale
    """,
    responses={
        200: {
            "description": "✅ Riepilogo engagement recuperato",
            "content": {
                "application/json": {
                    "example": {
                        "total_likes": 15420,
                        "total_comments": 2890,
                        "total_shares": 1156,
                        "average_sentiment": 0.72
                    }
                }
            }
        },
        404: {"description": "❌ Account non trovato o senza dati"}
    }
)
async def get_engagement_summary(
    account_id: int,
    user = Depends(get_current_user)
):
    """
    Genera un riepilogo completo delle metriche di engagement per l'account.
    
    Ideale per:
    - Report mensili/trimestrali
    - Valutazione ROI social media
    - Benchmark con competitor
    - KPI dashboard esecutiva
    """
    tracker = EngagementTracker()
    try:
        return tracker.get_engagement_summary(account_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"❌ {str(e)}")