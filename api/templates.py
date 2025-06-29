from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Optional, List
from pydantic import BaseModel, Field
from services.templates import TemplateManager
from auth import get_current_user

router = APIRouter(
    prefix="/templates", 
    tags=["📝 Template e Modelli"],
    responses={
        404: {"description": "Template non trovato"},
        400: {"description": "Dati non validi"},
        401: {"description": "Non autorizzato"}
    }
)

class TemplateCreate(BaseModel):
    name: str = Field(
        ..., 
        description="📛 Nome del template", 
        example="Post Promozionale",
        min_length=3,
        max_length=100
    )
    content: str = Field(
        ..., 
        description="📝 Contenuto del template con variabili {variabile}", 
        example="🎉 Scopri {prodotto}! Solo oggi {sconto}% di sconto! #promo #{categoria}",
        min_length=10,
        max_length=2000
    )
    variables: Optional[Dict[str, str]] = Field(
        None, 
        description="🔧 Variabili predefinite del template", 
        example={"prodotto": "Nome prodotto", "sconto": "20", "categoria": "tech"}
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "🎯 Post Promozionale Prodotto",
                "content": "🌟 Novità in arrivo! \n\n✨ {prodotto} è finalmente disponibile!\n💰 Prezzo speciale: {prezzo}\n📦 Disponibile su {piattaforma}\n\n#lancio #{categoria} #novità",
                "variables": {
                    "prodotto": "Il nostro nuovo servizio",
                    "prezzo": "€29.99",
                    "piattaforma": "il nostro store",
                    "categoria": "tech"
                }
            }
        }

class TemplateResponse(BaseModel):
    id: int = Field(..., description="🆔 ID univoco del template")
    name: str = Field(..., description="📛 Nome del template")
    content: str = Field(..., description="📝 Contenuto del template")
    variables: Dict[str, str] = Field(..., description="🔧 Variabili disponibili")

class TemplateApplyRequest(BaseModel):
    template_id: int = Field(
        ..., 
        description="🆔 ID del template da applicare", 
        ge=1
    )
    variables: Dict[str, str] = Field(
        ..., 
        description="🔧 Valori delle variabili da sostituire",
        example={"prodotto": "iPhone 15", "sconto": "15", "categoria": "smartphone"}
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "template_id": 1,
                "variables": {
                    "prodotto": "iPhone 15 Pro",
                    "prezzo": "€1199",
                    "piattaforma": "Apple Store",
                    "categoria": "smartphone"
                }
            }
        }

@router.post(
    "/", 
    response_model=TemplateResponse,
    summary="📝 Crea un nuovo template",
    description="""
    ## 🎨 Crea template riutilizzabili per i tuoi post
    
    I template ti permettono di:
    - **⚡ Velocizzare** la creazione di contenuti
    - **🎯 Mantenere coerenza** nel messaging
    - **🔧 Personalizzare** facilmente i contenuti
    - **📊 Standardizzare** tipologie di post
    
    ### 💡 Come funzionano le variabili:
    Usa la sintassi `{nome_variabile}` nel contenuto:
    - `{prodotto}` → Nome del prodotto
    - `{prezzo}` → Prezzo del prodotto  
    - `{sconto}` → Percentuale di sconto
    - `{categoria}` → Categoria del prodotto
    
    ### 🎯 Esempi di template utili:
    - **Promozionali**: Offerte e sconti
    - **Educativi**: Tips e consigli
    - **Engagement**: Domande e sondaggi
    - **Annunci**: Novità e aggiornamenti
    """,
    responses={
        200: {
            "description": "✅ Template creato con successo",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "🎯 Post Promozionale",
                        "content": "🌟 Scopri {prodotto}! Solo oggi {sconto}% di sconto!",
                        "variables": {
                            "prodotto": "Nome prodotto",
                            "sconto": "20"
                        }
                    }
                }
            }
        }
    }
)
async def create_template(
    template: TemplateCreate,
    user = Depends(get_current_user)
):
    """
    Crea un nuovo template per post ricorrenti.
    
    Perfetto per:
    - Standardizzare i messaggi aziendali
    - Velocizzare la creazione contenuti
    - Mantenere coerenza nel brand
    """
    manager = TemplateManager()
    try:
        return manager.create_template(
            name=template.name,
            content=template.content,
            variables=template.variables
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"❌ Errore nella creazione template: {str(e)}")

@router.get(
    "/", 
    response_model=List[TemplateResponse],
    summary="📋 Lista tutti i template disponibili",
    description="""
    ## 📚 Visualizza tutti i template salvati
    
    Ottieni la lista completa dei template disponibili:
    - **📝 Template personali** creati da te
    - **🎨 Template predefiniti** del sistema
    - **🔧 Variabili disponibili** per ogni template
    - **📊 Statistiche utilizzo** (prossimamente)
    
    ### 💡 Usa questa lista per:
    - Scegliere il template giusto per ogni occasione
    - Vedere quali variabili sono necessarie
    - Organizzare i tuoi template
    - Pianificare nuovi contenuti
    
    ### 🎯 Tipi di template disponibili:
    - **Promozionali** 🎯: Per offerte e sconti
    - **Educativi** 📚: Per tips e tutorial
    - **Engagement** 💬: Per domande e sondaggi
    - **Annunci** 📢: Per news e aggiornamenti
    """,
    responses={
        200: {
            "description": "✅ Lista template recuperata",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "name": "🎯 Promo Prodotto",
                            "content": "🌟 Scopri {prodotto}! Sconto {sconto}%",
                            "variables": {"prodotto": "Nome", "sconto": "20"}
                        },
                        {
                            "id": 2,
                            "name": "📚 Tip Educativo",
                            "content": "💡 Lo sapevi che {fatto}? #tips #{categoria}",
                            "variables": {"fatto": "Fatto interessante", "categoria": "tech"}
                        }
                    ]
                }
            }
        }
    }
)
async def list_templates(user = Depends(get_current_user)):
    """
    Recupera tutti i template disponibili per l'utente.
    
    Include template personali e predefiniti del sistema.
    """
    manager = TemplateManager()
    return manager.list_templates()

@router.post(
    "/apply",
    summary="🎨 Applica un template con variabili personalizzate",
    description="""
    ## ✨ Genera contenuto da un template esistente
    
    Trasforma un template in contenuto pronto per la pubblicazione:
    - **🔧 Sostituisce le variabili** con i tuoi valori
    - **✅ Valida il contenuto** generato
    - **📝 Restituisce testo** pronto per l'uso
    - **🎯 Mantiene formattazione** ed emoji
    
    ### 💡 Come funziona:
    1. Scegli un template dalla lista
    2. Fornisci i valori per le variabili richieste
    3. Ricevi il contenuto personalizzato
    4. Copia e usa nei tuoi post!
    
    ### 🔧 Esempio pratico:
    **Template**: `"🌟 Scopri {prodotto}! Sconto {sconto}%"`
    **Variabili**: `{"prodotto": "iPhone 15", "sconto": "20"}`
    **Risultato**: `"🌟 Scopri iPhone 15! Sconto 20%"`
    """,
    responses={
        200: {
            "description": "✅ Template applicato con successo",
            "content": {
                "application/json": {
                    "example": {
                        "content": "🌟 Scopri iPhone 15 Pro! Solo oggi 20% di sconto! #promo #smartphone"
                    }
                }
            }
        },
        404: {"description": "❌ Template non trovato"},
        400: {"description": "⚠️ Variabili mancanti o non valide"}
    }
)
async def apply_template(
    request: TemplateApplyRequest,
    user = Depends(get_current_user)
):
    """
    Applica un template sostituendo le variabili con valori personalizzati.
    
    Perfetto per:
    - Generare rapidamente contenuti personalizzati
    - Mantenere coerenza nel messaging
    - Velocizzare il workflow di posting
    """
    manager = TemplateManager()
    try:
        return {
            "content": manager.apply_template(
                request.template_id,
                request.variables
            )
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"❌ Errore nell'applicazione template: {str(e)}")

@router.delete(
    "/{template_id}",
    summary="🗑️ Elimina un template",
    description="""
    ## ❌ Rimuovi un template non più necessario
    
    Elimina definitivamente un template:
    - **🗑️ Rimozione permanente** dal sistema
    - **⚠️ Operazione irreversibile**
    - **📊 Statistiche conservate** per report
    
    ### 💡 Prima di eliminare:
    - Assicurati che non sia utilizzato in post programmati
    - Considera di esportare il contenuto se serve
    - Verifica che non sia condiviso con altri utenti
    
    ### 🔒 Limitazioni:
    - Non puoi eliminare template predefiniti del sistema
    - Solo i tuoi template personali possono essere rimossi
    """,
    responses={
        200: {
            "description": "✅ Template eliminato con successo",
            "content": {
                "application/json": {
                    "example": {"message": "✅ Template eliminato con successo"}
                }
            }
        },
        404: {"description": "❌ Template non trovato"},
        403: {"description": "🔒 Non autorizzato a eliminare questo template"}
    }
)
async def delete_template(
    template_id: int,
    user = Depends(get_current_user)
):
    """
    Elimina definitivamente un template.
    
    ⚠️ Attenzione: Operazione irreversibile!
    """
    manager = TemplateManager()
    if not manager.delete_template(template_id):
        raise HTTPException(status_code=404, detail="❌ Template non trovato o non eliminabile")
    return {"message": "✅ Template eliminato con successo"}