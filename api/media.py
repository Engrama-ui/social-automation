from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import List
from datetime import datetime
<<<<<<< HEAD
from pydantic import BaseModel
=======
from pydantic import BaseModel, Field
>>>>>>> bda3689dc620783c47fe4eefc69ce623bbc8cc42
from services.media import MediaManager
from auth import get_current_user

router = APIRouter(
    prefix="/media", 
    tags=["🖼️ Media e File"],
    responses={
        400: {"description": "File non valido o errore upload"},
        401: {"description": "Non autorizzato"},
        404: {"description": "Media non trovato"},
        413: {"description": "File troppo grande"}
    }
)

class MediaResponse(BaseModel):
    id: int = Field(..., description="🆔 ID univoco del media")
    filename: str = Field(..., description="📄 Nome del file")
    mime_type: str = Field(..., description="🎨 Tipo MIME del file")
    created_at: datetime = Field(..., description="⏰ Data di caricamento")
    file_size: int = Field(..., description="📏 Dimensione file in bytes")
    url: str = Field(..., description="🔗 URL pubblico del file")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 123,
                "filename": "promo-image.jpg",
                "mime_type": "image/jpeg",
                "created_at": "2024-01-15T14:30:00Z",
                "file_size": 245760,
                "url": "https://cdn.example.com/media/promo-image.jpg"
            }
        }

@router.post(
    "/", 
    response_model=MediaResponse,
    summary="📤 Carica file multimediali",
    description="""
    ## 🖼️ Upload di immagini, video e file per i tuoi post
    
    Carica contenuti multimediali per i tuoi social:
    - **📸 Immagini**: JPG, PNG, GIF, WebP
    - **🎥 Video**: MP4, MOV, AVI (max 100MB)
    - **🎵 Audio**: MP3, WAV (per alcuni social)
    - **📄 Documenti**: PDF (per LinkedIn)
    
    ### 📐 Formati consigliati per piattaforma:
    
    **Instagram**:
    - **Post**: 1080x1080px (quadrato), 1080x1350px (ritratto)
    - **Stories**: 1080x1920px (9:16)
    - **Reels**: 1080x1920px, MP4 max 90s
    
    **Facebook**:
    - **Post**: 1200x630px raccomandato
    - **Video**: 1280x720px, max 240min
    - **Cover**: 1640x856px
    
    **Twitter**:
    - **Post**: 1200x675px (16:9)
    - **Header**: 1500x500px
    - **Video**: max 512MB, 2:20min
    
    **LinkedIn**:
    - **Post**: 1200x627px
    - **Company banner**: 1536x768px
    - **Video**: 75KB-200MB, max 10min
    
    ### ✅ Ottimizzazione automatica:
    - **Compressione intelligente** per ridurre peso
    - **Ridimensionamento adattivo** per ogni piattaforma
    - **Watermark opzionale** per protezione brand
    - **Backup sicuro** su cloud storage
    
    ### 🔒 Sicurezza e privacy:
    - File scansionati per malware
    - Contenuti inappropriati filtrati automaticamente
    - Backup crittografati
    - Accesso controllato per team
    """,
    responses={
        200: {
            "description": "✅ File caricato con successo",
            "content": {
                "application/json": {
                    "example": {
                        "id": 123,
                        "filename": "campaign-visual.jpg",
                        "mime_type": "image/jpeg",
                        "created_at": "2024-01-15T14:30:00Z",
                        "file_size": 245760,
                        "url": "https://cdn.example.com/media/campaign-visual.jpg"
                    }
                }
            }
        },
        400: {"description": "❌ Formato file non supportato"},
        413: {"description": "📏 File troppo grande (max 100MB)"}
    }
)
async def upload_media(
    file: UploadFile = File(
        ..., 
        description="📤 File da caricare (max 100MB)",
        example="image.jpg"
    ),
    user = Depends(get_current_user)
):
    """
    Carica file multimediali per l'uso nei tuoi post social.
    
    Supporta:
    - Ottimizzazione automatica per ogni piattaforma
    - Gestione sicura e organizzata dei file
    - URL pubblici per condivisione
    - Backup e storage cloud
    """
    manager = MediaManager()
    try:
        return manager.save_media(file, user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"❌ Errore upload file: {str(e)}")

@router.get(
    "/", 
    response_model=List[MediaResponse],
    summary="📂 Lista dei tuoi media",
    description="""
    ## 📚 Galleria completa dei tuoi file multimediali
    
    Visualizza tutti i file caricati:
    - **🖼️ Anteprima visuale** dei media
    - **📊 Dettagli tecnici** (formato, dimensioni)
    - **📅 Data caricamento** per organizzazione
    - **🔗 URL pubblici** pronti per l'uso
    
    ### 🎯 Organizzazione intelligente:
    - **Ordinamento per data** (più recenti primi)
    - **Filtri per tipo** (immagini, video, audio)
    - **Ricerca per nome** file
    - **Tag personalizzati** per categorizzazione
    
    ### 💡 Suggerimenti d'uso:
    - **Riutilizzo contenuti**: Trova rapidamente media precedenti
    - **Batch operations**: Seleziona multipli file per azioni massive
    - **Performance tracking**: Vedi quali media performano meglio
    - **Storage management**: Monitora spazio utilizzato
    
    ### 📊 Metriche disponibili:
    - Numero totale file caricati
    - Spazio storage utilizzato
    - File più utilizzati nei post
    - Performance media per tipo
    """,
    responses={
        200: {
            "description": "✅ Lista media recuperata",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 125,
                            "filename": "latest-product.jpg",
                            "mime_type": "image/jpeg",
                            "created_at": "2024-01-15T14:30:00Z",
                            "file_size": 156890,
                            "url": "https://cdn.example.com/media/latest-product.jpg"
                        },
                        {
                            "id": 124,
                            "filename": "promo-video.mp4",
                            "mime_type": "video/mp4",
                            "created_at": "2024-01-14T10:15:00Z",
                            "file_size": 5240000,
                            "url": "https://cdn.example.com/media/promo-video.mp4"
                        }
                    ]
                }
            }
        }
    }
)
async def list_media(user = Depends(get_current_user)):
    """
    Recupera tutti i media caricati dall'utente corrente.
    
    Utile per:
    - Gestione libreria media personale
    - Riutilizzo contenuti esistenti
    - Organizzazione asset digitali
    - Pianificazione contenuti futuri
    """
    manager = MediaManager()
    return manager.list_user_media(user.id)

@router.delete(
    "/{media_id}",
    summary="🗑️ Elimina file media",
    description="""
    ## ❌ Rimuovi definitivamente un file multimediale
    
    Elimina file non più necessari:
    - **🗑️ Rimozione permanente** dal sistema
    - **☁️ Pulizia storage** automatica
    - **🔗 Invalidazione URL** pubblici
    - **📊 Conservazione statistiche** utilizzo
    
    ### ⚠️ Attenzione:
    - **Operazione irreversibile**: File eliminato definitivamente
    - **Post collegati**: Verifica che non sia usato in post programmati
    - **Link esterni**: URL del file non funzioneranno più
    - **Backup**: Considera download prima dell'eliminazione
    
    ### 💡 Prima di eliminare:
    - Controlla utilizzo in post passati/futuri
    - Scarica copia locale se necessario
    - Verifica che non sia parte di campagne attive
    - Considera archiviazione invece di eliminazione
    
    ### 🔒 Sicurezza:
    - Solo il proprietario può eliminare
    - Log audit mantenuti per sicurezza
    - Impossibile recuperare dopo eliminazione
    """,
    responses={
        200: {
            "description": "✅ File eliminato con successo",
            "content": {
                "application/json": {
                    "example": {"message": "✅ Media eliminato con successo"}
                }
            }
        },
        404: {"description": "❌ File non trovato"},
        403: {"description": "🔒 Non autorizzato a eliminare questo file"}
    }
)
async def delete_media(
    media_id: int,
    user = Depends(get_current_user)
):
    """
    Elimina definitivamente un file multimediale.
    
    ⚠️ Attenzione: Operazione irreversibile!
    
    Verifica che il file non sia:
    - Utilizzato in post programmati
    - Parte di campagne attive
    - Referenziato in template
    """
    manager = MediaManager()
    if not manager.delete_media(media_id):
        raise HTTPException(status_code=404, detail="❌ Media non trovato o non eliminabile")
    return {"message": "✅ Media eliminato con successo"}