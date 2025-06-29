from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict
from pydantic import BaseModel, Field
from services.hashtags import HashtagOptimizer
from auth import get_current_user

router = APIRouter(
    prefix="/hashtags", 
    tags=["🏷️ Hashtag e Ottimizzazione"],
    responses={
        404: {"description": "Hashtag non trovato"},
        400: {"description": "Parametri non validi"},
        401: {"description": "Non autorizzato"}
    }
)

class HashtagResearchResponse(BaseModel):
    hashtag: str = Field(..., description="🏷️ Hashtag analizzato")
    popularity: float = Field(..., description="📊 Popolarità (0-100)")
    related_hashtags: List[str] = Field(..., description="🔗 Hashtag correlati")
    recent_posts: int = Field(..., description="📈 Post recenti con questo hashtag")
    
    class Config:
        json_schema_extra = {
            "example": {
                "hashtag": "#marketing",
                "popularity": 87.5,
                "related_hashtags": ["#digitalmarketing", "#socialmedia", "#business"],
                "recent_posts": 15420
            }
        }

class HashtagPerformanceResponse(BaseModel):
    hashtag: str = Field(..., description="🏷️ Hashtag analizzato")
    total_posts: int = Field(..., description="📊 Numero totale di post")
    total_engagement: int = Field(..., description="💙 Engagement totale")
    average_engagement: float = Field(..., description="📈 Engagement medio per post")

class HashtagSuggestionRequest(BaseModel):
    content: str = Field(
        ..., 
        description="📝 Contenuto del post per suggerimenti", 
        example="Scopri i nostri nuovi prodotti tech innovativi per il 2024!",
        min_length=10,
        max_length=500
    )
    limit: int = Field(
        5, 
        description="🔢 Numero massimo di hashtag suggeriti", 
        ge=1, 
        le=30,
        example=5
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "content": "Lancio del nostro nuovo smartphone con tecnologia AI avanzata!",
                "limit": 8
            }
        }

@router.get(
    "/research/{hashtag}", 
    response_model=HashtagResearchResponse,
    summary="🔍 Ricerca approfondita su un hashtag",
    description="""
    ## 📊 Analisi completa di un hashtag specifico
    
    Ottieni insights dettagliati su qualsiasi hashtag:
    - **📈 Popolarità attuale** e trend nel tempo
    - **🔗 Hashtag correlati** per espandere reach
    - **📊 Volume di post** recenti
    - **🎯 Suggerimenti strategici** per l'uso
    
    ### 💡 Come interpretare i dati:
    - **Popolarità 80-100**: Hashtag molto popolare, alta competizione
    - **Popolarità 50-79**: Buon equilibrio visibilità/competizione  
    - **Popolarità 20-49**: Nicchia specifica, meno competizione
    - **Popolarità 0-19**: Hashtag nuovo o molto specifico
    
    ### 🎯 Strategie consigliate:
    - **Mix di popolarità**: Usa hashtag popolari + di nicchia
    - **Hashtag correlati**: Aumentano discovery organica
    - **Monitoraggio trend**: Controlla regolarmente la popolarità
    """,
    responses={
        200: {
            "description": "✅ Ricerca completata con successo",
            "content": {
                "application/json": {
                    "example": {
                        "hashtag": "#marketing",
                        "popularity": 87.5,
                        "related_hashtags": ["#digitalmarketing", "#socialmedia", "#business", "#branding"],
                        "recent_posts": 15420
                    }
                }
            }
        },
        404: {"description": "❌ Hashtag non trovato nei nostri database"}
    }
)
async def research_hashtag(
    hashtag: str,
    user = Depends(get_current_user)
):
    """
    Analizza un hashtag specifico per ottimizzare la strategia.
    
    Perfetto per:
    - Ricerca di mercato su hashtag
    - Pianificazione strategica contenuti
    - Identificazione opportunità di nicchia
    - Analisi competitor
    """
    optimizer = HashtagOptimizer()
    try:
        return optimizer.research_hashtag(hashtag)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"❌ Errore nella ricerca hashtag: {str(e)}")

@router.get(
    "/performance/{hashtag_id}", 
    response_model=HashtagPerformanceResponse,
    summary="📈 Performance di un hashtag specifico",
    description="""
    ## 📊 Analisi delle performance di un hashtag
    
    Monitora l'efficacia dei tuoi hashtag:
    - **📊 Numero totale** di post pubblicati
    - **💙 Engagement totale** generato
    - **📈 Engagement medio** per post
    - **🎯 ROI dell'hashtag** (return on investment)
    
    ### 💡 Metriche chiave:
    - **Total Posts**: Volume di contenuti con l'hashtag
    - **Total Engagement**: Like + commenti + condivisioni
    - **Average Engagement**: Media engagement per post
    - **Trend**: Crescita/decrescita nel tempo
    
    ### 🎯 Come usare questi dati:
    - **Alto engagement**: Hashtag efficace, continua a usarlo
    - **Basso engagement**: Considera alternative o combinazioni
    - **Trend positivo**: Aumenta la frequenza d'uso
    - **Trend negativo**: Riduci o sostituisci
    """,
    responses={
        200: {
            "description": "✅ Performance recuperate con successo",
            "content": {
                "application/json": {
                    "example": {
                        "hashtag": "#marketing",
                        "total_posts": 1250,
                        "total_engagement": 45600,
                        "average_engagement": 36.48
                    }
                }
            }
        }
    }
)
async def get_hashtag_performance(
    hashtag_id: int,
    user = Depends(get_current_user)
):
    """
    Analizza le performance di un hashtag specifico nei tuoi post.
    
    Utile per:
    - Valutare efficacia hashtag
    - Ottimizzare strategia contenuti
    - Identificare hashtag top performer
    """
    optimizer = HashtagOptimizer()
    try:
        return optimizer.track_performance(hashtag_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"❌ Errore nel recupero performance: {str(e)}")

@router.post(
    "/suggestions", 
    response_model=List[str],
    summary="💡 Suggerimenti hashtag intelligenti",
    description="""
    ## 🤖 AI-powered hashtag suggestions
    
    Ottieni hashtag ottimizzati per il tuo contenuto:
    - **🎯 Analisi del contenuto** con AI
    - **📊 Hashtag popolari** per il tuo settore
    - **🔍 Hashtag di nicchia** per reach mirato
    - **⚖️ Bilanciamento** tra popolarità e competizione
    
    ### 💡 Come funziona l'algoritmo:
    1. **Analisi semantica** del tuo contenuto
    2. **Identificazione keywords** chiave
    3. **Mappatura hashtag** rilevanti
    4. **Ranking per efficacia** potenziale
    5. **Filtro duplicati** e spam
    
    ### 🎯 Strategie integrate:
    - **30% hashtag popolari** (broad reach)
    - **50% hashtag medi** (target specifico)  
    - **20% hashtag nicchia** (engagement alto)
    
    ### 📝 Tips per migliori risultati:
    - Scrivi contenuto descrittivo e specifico
    - Includi settore/categoria di riferimento
    - Menziona target audience se rilevante
    """,
    responses={
        200: {
            "description": "✅ Suggerimenti generati con successo",
            "content": {
                "application/json": {
                    "example": [
                        "#marketing",
                        "#digitalmarketing", 
                        "#socialmedia",
                        "#business",
                        "#entrepreneur"
                    ]
                }
            }
        }
    }
)
async def get_hashtag_suggestions(
    request: HashtagSuggestionRequest,
    user = Depends(get_current_user)
):
    """
    Genera hashtag ottimizzati usando AI per massimizzare reach ed engagement.
    
    Perfetto per:
    - Contenuti nuovi senza hashtag
    - Ottimizzazione post esistenti
    - Ricerca hashtag di nicchia
    - Strategia multi-piattaforma
    """
    optimizer = HashtagOptimizer()
    try:
        return optimizer.get_suggestions(request.content, request.limit)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"❌ Errore nella generazione suggerimenti: {str(e)}")

@router.get(
    "/trending", 
    response_model=List[Dict],
    summary="🔥 Hashtag di tendenza per piattaforma",
    description="""
    ## 📈 Scopri gli hashtag più caldi del momento
    
    Resta aggiornato sui trend:
    - **🔥 Hashtag virali** del momento
    - **📊 Crescita in tempo reale** 
    - **🎯 Filtra per piattaforma** specifica
    - **📅 Trend storici** e previsioni
    
    ### 🌐 Piattaforme supportate:
    - **Instagram**: Trend visual e lifestyle
    - **Twitter**: News, tech, discussioni
    - **LinkedIn**: Business e professionale
    - **TikTok**: Entertainment e viral
    - **All**: Aggregato multi-piattaforma
    
    ### 💡 Come sfruttare i trend:
    - **React velocemente** ai trend emergenti
    - **Adatta contenuti** a trend rilevanti
    - **Evita trend** in declino
    - **Monitora competitor** sui trend
    
    ### ⚠️ Best practices:
    - Non forzare hashtag non pertinenti
    - Verifica relevanza per il tuo brand
    - Combina trend + hashtag di nicchia
    - Monitora performance trend adottati
    """,
    responses={
        200: {
            "description": "✅ Trend recuperati con successo",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "hashtag": "#AI2024",
                            "platform": "all",
                            "growth_rate": 156.7,
                            "total_posts": 89420,
                            "category": "technology"
                        },
                        {
                            "hashtag": "#sustainability",
                            "platform": "instagram", 
                            "growth_rate": 98.3,
                            "total_posts": 234560,
                            "category": "lifestyle"
                        }
                    ]
                }
            }
        }
    }
)
async def get_trending_hashtags(
    platform: str = Query(
        "all",
        description="🌐 Piattaforma per filtrare i trend",
        pattern="^(all|instagram|twitter|linkedin|tiktok)$"
    ),
    user = Depends(get_current_user)
):
    """
    Scopri hashtag di tendenza per cavalcare i trend del momento.
    
    Ideale per:
    - Content strategy aggiornata
    - Opportunità viral marketing
    - Ricerca trend emergenti
    - Benchmarking competitor
    """
    optimizer = HashtagOptimizer()
    try:
        return optimizer.get_trending(platform)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"❌ Errore nel recupero trend: {str(e)}")