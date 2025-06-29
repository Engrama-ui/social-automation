from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from services.scheduler import ContentScheduler
from auth import get_current_user

router = APIRouter(
    prefix="/content", 
    tags=["📝 Gestione Contenuti"],
    responses={
        404: {"description": "Contenuto non trovato"},
        400: {"description": "Dati non validi"},
        401: {"description": "Non autorizzato"}
    }
)

class PostCreate(BaseModel):
    account_id: int = Field(
        ..., 
        description="🆔 ID dell'account social media", 
        example=1,
        ge=1
    )
    content: str = Field(
        ..., 
        description="📝 Testo del post da pubblicare", 
        example="🌟 Scopri le novità del nostro servizio! #innovation #tech",
        min_length=1,
        max_length=2000
    )
    media_urls: Optional[List[str]] = Field(
        None, 
        description="🖼️ Lista di URL delle immagini/video (opzionale)", 
        example=["https://example.com/image1.jpg", "https://example.com/video1.mp4"]
    )
    scheduled_time: Optional[datetime] = Field(
        None, 
        description="⏰ Data e ora di pubblicazione (se non specificata, pubblica subito)", 
        example="2024-06-30T14:30:00"
    )

    class Config:
        json_json_schema_extra = {
            "example": {
                "account_id": 1,
                "content": "🎉 Lancio del nostro nuovo prodotto! Non perdertelo! #lancio #novità #prodotto",
                "media_urls": ["https://example.com/product-image.jpg"],
                "scheduled_time": "2024-06-30T14:30:00"
            }
        }

class PostResponse(BaseModel):
    id: int = Field(..., description="🆔 ID univoco del post")
    account_id: int = Field(..., description="🆔 ID dell'account")
    content: str = Field(..., description="📝 Contenuto del post")
    media_urls: List[str] = Field(..., description="🖼️ URL dei media allegati")
    scheduled_time: datetime = Field(..., description="⏰ Data/ora di pubblicazione")
    status: str = Field(..., description="📊 Stato del post (scheduled/published/failed)")

@router.post(
    "/", 
    response_model=PostResponse,
    summary="📝 Crea e programma un nuovo post",
    description="""
    ## 🚀 Crea un nuovo post per i social media
    
    Questo endpoint ti permette di:
    - **📱 Pubblicare immediatamente** su uno o più social network
    - **⏰ Programmare la pubblicazione** per un momento specifico
    - **🖼️ Allegare media** (immagini, video) al tuo post
    - **🎯 Targetizzare account specifici**
    
    ### 💡 Suggerimenti:
    - Usa emoji per rendere i post più accattivanti
    - Includi 1-3 hashtag rilevanti per aumentare la visibilità
    - Gli orari migliori per pubblicare sono 9-11 e 19-21
    - Le immagini aumentano l'engagement del 650%
    
    ### ⚠️ Note importanti:
    - Se `scheduled_time` non è specificato, il post viene pubblicato immediatamente
    - Assicurati che l'account_id sia valido e attivo
    - I media_urls devono puntare a file accessibili pubblicamente
    """,
    responses={
        200: {
            "description": "✅ Post creato con successo",
            "content": {
                "application/json": {
                    "example": {
                        "id": 123,
                        "account_id": 1,
                        "content": "🎉 Lancio del nostro nuovo prodotto!",
                        "media_urls": ["https://example.com/image.jpg"],
                        "scheduled_time": "2024-06-30T14:30:00",
                        "status": "scheduled"
                    }
                }
            }
        },
        400: {"description": "❌ Dati del post non validi"},
        401: {"description": "🔒 Autenticazione richiesta"},
        422: {"description": "⚠️ Errore di validazione dei dati"}
    }
)
async def schedule_post(
    post: PostCreate,
    user = Depends(get_current_user)
):
    """
    Crea e programma un nuovo post sui social media.
    
    Perfetto per:
    - Pubblicazioni immediate
    - Programmazione di contenuti
    - Gestione multi-account
    - Allegare media ai post
    """
    scheduler = ContentScheduler()
    try:
        scheduled_post = scheduler.schedule_post(
            account_id=post.account_id,
            content=post.content,
            media_urls=post.media_urls,
            scheduled_time=post.scheduled_time
        )
        return scheduled_post
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get(
    "/{account_id}", 
    response_model=List[PostResponse],
    summary="📋 Visualizza post programmati",
    description="""
    ## 📅 Ottieni tutti i post programmati per un account
    
    Questo endpoint ti permette di:
    - **📋 Visualizzare tutti i post** programmati per un account specifico
    - **🔍 Filtrare per periodo** utilizzando start_time e end_time
    - **📊 Monitorare lo stato** dei post (pubblicati, programmati, falliti)
    - **⏰ Pianificare meglio** i contenuti futuri
    
    ### 💡 Suggerimenti:
    - Usa i filtri di data per vedere solo i post di un periodo specifico
    - Controlla regolarmente lo stato dei post programmati
    - Pianifica i contenuti con almeno una settimana di anticipo
    
    ### 📊 Stati possibili:
    - `scheduled`: Post programmato, in attesa di pubblicazione
    - `published`: Post pubblicato con successo
    - `failed`: Pubblicazione fallita, richiede attenzione
    - `cancelled`: Post cancellato dall'utente
    """,
    responses={
        200: {
            "description": "✅ Lista dei post recuperata con successo",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 123,
                            "account_id": 1,
                            "content": "🎉 Post programmato per oggi!",
                            "media_urls": ["https://example.com/image.jpg"],
                            "scheduled_time": "2024-06-30T14:30:00",
                            "status": "scheduled"
                        }
                    ]
                }
            }
        },
        404: {"description": "❌ Account non trovato"},
        401: {"description": "🔒 Autenticazione richiesta"}
    }
)
async def get_scheduled_posts(
    account_id: int,
    start_time: Optional[datetime] = Query(None, description="📅 Data/ora di inizio filtro (opzionale)"),
    end_time: Optional[datetime] = Query(None, description="📅 Data/ora di fine filtro (opzionale)"),
    user = Depends(get_current_user)
):
    """
    Recupera tutti i post programmati per un account specifico.
    
    Utile per:
    - Visualizzare il calendario dei contenuti
    - Controllare lo stato delle pubblicazioni
    - Pianificare nuovi contenuti
    """
    scheduler = ContentScheduler()
    return scheduler.get_scheduled_posts(
        account_id=account_id,
        start_time=start_time,
        end_time=end_time
    )

@router.delete(
    "/{post_id}",
    summary="🗑️ Cancella un post programmato",
    description="""
    ## ❌ Cancella un post programmato
    
    Questo endpoint ti permette di:
    - **🗑️ Cancellare definitivamente** un post programmato
    - **⏰ Evitare pubblicazioni** non più desiderate
    - **🔄 Liberare slot** nel calendario dei contenuti
    
    ### ⚠️ Attenzione:
    - Un post cancellato **non può essere recuperato**
    - Puoi cancellare solo post con stato `scheduled`
    - I post già pubblicati non possono essere cancellati
    
    ### 💡 Alternativa:
    Se vuoi modificare un post invece di cancellarlo, cancellalo prima e poi creane uno nuovo con i contenuti aggiornati.
    """,
    responses={
        200: {
            "description": "✅ Post cancellato con successo",
            "content": {
                "application/json": {
                    "example": {"message": "✅ Post cancellato con successo"}
                }
            }
        },
        404: {"description": "❌ Post non trovato o già pubblicato"},
        401: {"description": "🔒 Autenticazione richiesta"}
    }
)
async def cancel_post(
    post_id: int,
    user = Depends(get_current_user)
):
    """
    Cancella un post programmato.
    
    ⚠️ Operazione irreversibile - il post verrà eliminato definitivamente.
    """
    scheduler = ContentScheduler()
    if not scheduler.cancel_post(post_id):
        raise HTTPException(status_code=404, detail="❌ Post non trovato o non cancellabile")
    return {"message": "✅ Post cancellato con successo"}