from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from services.platforms import PlatformManager
from auth import get_current_user

router = APIRouter(
    prefix="/platforms", 
    tags=["🌐 Piattaforme Social"],
    responses={
        400: {"description": "Errore nella richiesta"},
        401: {"description": "Non autorizzato"},
        404: {"description": "Risorsa non trovata"}
    }
)

class ConnectRequest(BaseModel):
    platform: str = Field(
        ..., 
        description="🌐 Nome della piattaforma social",
        example="instagram",
        pattern="^(instagram|facebook|twitter|linkedin|tiktok|youtube)$"
    )
    auth_data: Dict = Field(
        ..., 
        description="🔑 Dati di autenticazione per la piattaforma",
        example={
            "access_token": "your_access_token_here",
            "account_id": "your_account_id",
            "permissions": ["publish_content", "read_insights"]
        }
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "platform": "instagram",
                "auth_data": {
                    "access_token": "EAAG...xyz123",
                    "account_id": "17841400455970028",
                    "permissions": ["instagram_basic", "pages_show_list"]
                }
            }
        }

class PostRequest(BaseModel):
    content: str = Field(
        ..., 
        description="📝 Contenuto del post da pubblicare",
        example="🌟 Scopri le novità di oggi! #innovation #tech",
        min_length=1,
        max_length=2200
    )
    media_urls: Optional[List[str]] = Field(
        None, 
        description="🖼️ URL delle immagini/video da allegare",
        example=["https://example.com/image1.jpg", "https://example.com/video1.mp4"]
    )
    scheduled_time: Optional[str] = Field(
        None,
        description="⏰ Data/ora programmazione (ISO format)",
        example="2024-01-15T14:30:00Z"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "content": "🚀 Lancia il tuo business online! \n\n✨ Scopri i nostri servizi digitali\n💡 Consulenza gratuita disponibile\n\n#digitalbusiness #startup #innovation",
                "media_urls": [
                    "https://example.com/promo-image.jpg"
                ],
                "scheduled_time": "2024-01-15T14:30:00Z"
            }
        }

@router.post(
    "/connect",
    summary="🔗 Connetti account social",
    description="""
    ## 🌐 Collega una nuova piattaforma social al tuo account
    
    Connetti i tuoi profili social per pubblicare automaticamente:
    - **Instagram** 📸: Post, Stories, Reels
    - **Facebook** 👥: Post aziendali e personali
    - **Twitter** 🐦: Tweet e thread
    - **LinkedIn** 💼: Post professionali e aziendali
    - **TikTok** 🎵: Video brevi e creativi
    - **YouTube** 📺: Video e YouTube Shorts
    
    ### 🔐 Sicurezza e Privacy:
    - Connessioni crittografate end-to-end
    - Token di accesso memorizzati in sicurezza
    - Permessi minimi necessari richiesti
    - Revoca accesso in qualsiasi momento
    
    ### 📋 Requisiti per piattaforma:
    - **Instagram/Facebook**: Business Account richiesto
    - **Twitter**: Developer Account opzionale per features avanzate
    - **LinkedIn**: Company Page per post aziendali
    - **TikTok**: Creator Account raccomandato
    
    ### ⚠️ Note importanti:
    - Verifica permessi prima della connessione
    - Alcuni contenuti potrebbero richiedere revisione manuale
    - Rate limits applicati secondo policy delle piattaforme
    """,
    responses={
        200: {
            "description": "✅ Account connesso con successo",
            "content": {
                "application/json": {
                    "example": {
                        "account_id": 12345,
                        "platform": "instagram",
                        "username": "@mycompany",
                        "status": "connected",
                        "permissions": ["publish_content", "read_insights"]
                    }
                }
            }
        },
        400: {"description": "❌ Dati di autenticazione non validi"}
    }
)
async def connect_account(
    request: ConnectRequest,
    user = Depends(get_current_user)
):
    """
    Connette un nuovo account social alla piattaforma.
    
    Necessario per:
    - Pubblicare contenuti automaticamente
    - Accedere a insights e analytics
    - Gestire multiple piattaforme da un'unica dashboard
    - Programmare post multi-piattaforma
    """
    manager = PlatformManager()
    try:
        return manager.connect_account(request.platform, request.auth_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"❌ Errore connessione: {str(e)}")

@router.post(
    "/{account_id}/post",
    summary="📝 Pubblica contenuto su piattaforma",
    description="""
    ## 🚀 Pubblica contenuti su una piattaforma social specifica
    
    Caratteristiche della pubblicazione:
    - **📝 Contenuto ottimizzato** per ogni piattaforma
    - **🖼️ Media multipli** supportati (immagini/video)
    - **⏰ Scheduling avanzato** con fusi orari
    - **🎯 Targeting specifico** per piattaforma
    
    ### 📐 Limitazioni per piattaforma:
    - **Instagram**: Massimo 10 immagini, video <60s
    - **Twitter**: 280 caratteri, 4 immagini max
    - **LinkedIn**: 3000 caratteri, formato professionale
    - **TikTok**: Solo video, 15s-10min
    - **Facebook**: 63.206 caratteri, media illimitati
    
    ### 🎨 Best practices contenuto:
    - **Instagram**: Visual-first, hashtag strategici
    - **Twitter**: Conciso, trending hashtag
    - **LinkedIn**: Professionale, industry insights
    - **TikTok**: Creativo, trend-aware
    - **Facebook**: Community-focused, conversational
    
    ### ⏰ Scheduling intelligente:
    - Orari ottimali per ogni piattaforma
    - Fusi orari audience target
    - Evita sovrapposizioni cross-platform
    - Rispetta algoritmi piattaforme
    """,
    responses={
        200: {
            "description": "✅ Contenuto pubblicato con successo",
            "content": {
                "application/json": {
                    "example": {
                        "post_id": "18027351109156789",
                        "platform": "instagram",
                        "status": "published",
                        "url": "https://instagram.com/p/ABC123/",
                        "scheduled_time": "2024-01-15T14:30:00Z"
                    }
                }
            }
        },
        400: {"description": "⚠️ Contenuto non valido per la piattaforma"}
    }
)
async def post_content(
    account_id: int,
    request: PostRequest,
    user = Depends(get_current_user)
):
    """
    Pubblica contenuto su una specifica piattaforma social.
    
    Ideale per:
    - Pubblicazione immediata
    - Content scheduling
    - Cross-posting ottimizzato
    - Campagne coordinate
    """
    manager = PlatformManager()
    try:
        return manager.post_content(account_id, request.content, request.media_urls)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"❌ Errore pubblicazione: {str(e)}")

@router.get(
    "/{account_id}/insights",
    summary="📊 Analytics e insights account",
    description="""
    ## 📈 Dati analytics completi per l'account social
    
    Metriche disponibili per ottimizzare la strategia:
    - **👥 Audience Demographics**: Età, geografia, interessi
    - **📊 Performance Metrics**: Reach, impression, engagement
    - **⏰ Optimal Timing**: Migliori orari per pubblicare
    - **📈 Growth Trends**: Crescita follower e engagement
    
    ### 📊 Metriche per piattaforma:
    
    **Instagram**:
    - Reach, Impressions, Profile visits
    - Story views, Website clicks
    - Hashtag performance, Save rate
    
    **Facebook**:
    - Page views, Post engagement
    - Video retention, Link clicks  
    - Demographics audience
    
    **Twitter**:
    - Impressions, Engagements
    - Profile clicks, Follows
    - Top tweets performance
    
    **LinkedIn**:
    - Post views, Social actions
    - Follower demographics
    - Company page analytics
    
    ### 💡 Come usare questi dati:
    - **Audience insights**: Personalizza contenuti per target
    - **Timing optimization**: Pubblica quando audience è attiva
    - **Content performance**: Replica successi, evita flop
    - **Growth tracking**: Monitora KPI e obiettivi
    """,
    responses={
        200: {
            "description": "✅ Insights recuperati con successo",
            "content": {
                "application/json": {
                    "example": {
                        "account_info": {
                            "platform": "instagram",
                            "username": "@mycompany",
                            "followers": 12540
                        },
                        "performance": {
                            "reach": 45600,
                            "impressions": 78900,
                            "engagement_rate": 3.2
                        },
                        "audience": {
                            "top_city": "Milan",
                            "age_range": "25-34",
                            "gender_split": {"male": 45, "female": 55}
                        }
                    }
                }
            }
        }
    }
)
async def get_insights(
    account_id: int,
    user = Depends(get_current_user)
):
    """
    Recupera insights e analytics completi per l'account social.
    
    Essenziale per:
    - Ottimizzazione strategia contenuti
    - ROI measurement social media
    - Audience analysis e targeting
    - Competitive benchmarking
    """
    manager = PlatformManager()
    try:
        return manager.get_insights(account_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"❌ Errore recupero insights: {str(e)}")