from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from typing import List
from datetime import datetime
from pydantic import BaseModel, Field
from services.notifications import NotificationManager
from auth import get_current_user, get_current_user_ws

router = APIRouter(
    prefix="/notifications", 
    tags=["🔔 Notifiche e Avvisi"],
    responses={
        404: {"description": "Notifica non trovata"},
        401: {"description": "Non autorizzato"},
        400: {"description": "Richiesta non valida"}
    }
)

class NotificationResponse(BaseModel):
    id: int = Field(..., description="🆔 ID univoco della notifica")
    message: str = Field(..., description="💬 Messaggio della notifica")
    notification_type: str = Field(..., description="🎯 Tipo di notifica")
    timestamp: datetime = Field(..., description="⏰ Data e ora della notifica")
    read: bool = Field(..., description="👁️ Stato lettura notifica")
    priority: str = Field(..., description="⚡ Priorità (low, medium, high)")
    action_url: str = Field(None, description="🔗 URL azione opzionale")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 123,
                "message": "🎉 Il tuo post ha raggiunto 1000 like!",
                "notification_type": "engagement_milestone",
                "timestamp": "2024-01-15T14:30:00Z",
                "read": False,
                "priority": "medium",
                "action_url": "/dashboard/analytics"
            }
        }

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Field(..., description="🔑 Token di autenticazione")
):
    """
    ## 🔗 WebSocket per notifiche in tempo reale
    
    Connessione WebSocket per ricevere notifiche live:
    - **⚡ Notifiche istantanee** senza refresh
    - **🎯 Filtrate per utente** corrente
    - **📱 Push notifications** su tutti i dispositivi
    - **🔄 Reconnect automatico** in caso di disconnessione
    
    ### 🎯 Tipi di notifiche in tempo reale:
    - **📈 Milestone engagement**: Traguardi like/commenti raggiunti
    - **⚠️ Errori pubblicazione**: Problemi con post programmati
    - **✅ Conferme successo**: Post pubblicati correttamente
    - **🔔 Reminder**: Promemoria attività da completare
    - **📊 Report automatici**: Riepiloghi performance periodici
    
    ### 💡 Come utilizzare:
    ```javascript
    const ws = new WebSocket('ws://localhost:8000/notifications/ws?token=YOUR_TOKEN');
    ws.onmessage = (event) => {
        const notification = JSON.parse(event.data);
        showNotification(notification);
    };
    ```
    """
    user = get_current_user_ws(token)
    if not user:
        await websocket.close(code=1008)
        return
        
    manager = NotificationManager()
    await websocket.accept()
    manager.register(user.id, websocket)
    
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.unregister(user.id, websocket)

@router.get(
    "/", 
    response_model=List[NotificationResponse],
    summary="📬 Tutte le notifiche dell'utente",
    description="""
    ## 🔔 Centro notifiche completo
    
    Recupera tutte le notifiche per l'utente:
    - **📨 Notifiche non lette** evidenziate
    - **📅 Ordinate per data** (più recenti prime)
    - **🎯 Categorizzate per tipo** e priorità
    - **🔗 Azioni dirette** integrate
    
    ### 🎯 Tipi di notifiche:
    - **📈 engagement_milestone**: Traguardi raggiunti
    - **⚠️ post_error**: Errori in pubblicazione
    - **✅ post_success**: Conferme pubblicazione
    - **🔔 reminder**: Promemoria e scadenze
    - **📊 report**: Report automatici
    - **⚙️ system**: Aggiornamenti sistema
    
    ### ⚡ Livelli di priorità:
    - **🔴 High**: Richiede attenzione immediata
    - **🟠 Medium**: Importante ma non urgente
    - **🟢 Low**: Informativo, può essere rimandato
    
    ### 💡 Best practices:
    - Controlla notifiche regolarmente
    - Segna come lette quelle viste
    - Agisci su notifiche ad alta priorità
    - Configura preferenze notifiche
    """,
    responses={
        200: {
            "description": "✅ Notifiche recuperate con successo",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 125,
                            "message": "🎉 Il tuo post Instagram ha superato 500 like!",
                            "notification_type": "engagement_milestone",
                            "timestamp": "2024-01-15T14:30:00Z",
                            "read": False,
                            "priority": "medium",
                            "action_url": "/dashboard/analytics"
                        },
                        {
                            "id": 124,
                            "message": "✅ Post pubblicato con successo su Facebook",
                            "notification_type": "post_success",
                            "timestamp": "2024-01-15T12:00:00Z",
                            "read": True,
                            "priority": "low",
                            "action_url": null
                        }
                    ]
                }
            }
        }
    }
)
async def get_notifications(user = Depends(get_current_user)):
    """
    Recupera tutte le notifiche per l'utente corrente.
    
    Include:
    - Notifiche non lette evidenziate
    - Cronologia completa notifiche
    - Link azioni dirette quando disponibili
    - Informazioni priorità e categoria
    """
    manager = NotificationManager()
    return manager.get_user_notifications(user.id)

@router.post(
    "/{notification_id}/read",
    summary="👁️ Segna notifica come letta",
    description="""
    ## ✅ Gestione stato lettura notifiche
    
    Segna una notifica specifica come letta:
    - **👁️ Aggiorna stato visivo** nelle UI
    - **📊 Traccia engagement** con notifiche
    - **🔔 Riduce contatori** non lette
    - **📱 Sincronizza multi-device** stato lettura
    
    ### 💡 Comportamento:
    - Notifica scompare da "non lette"
    - Rimane visibile in cronologia completa
    - Stato sincronizzato su tutti i dispositivi
    - Non influenza notifiche future simili
    
    ### 🎯 Best practices:
    - Segna come letta dopo aver preso azione
    - Usa per tenere traccia di cosa hai già visto
    - Non necessario per notifiche automatiche
    - Aiuta a mantenere dashboard pulita
    """,
    responses={
        200: {
            "description": "✅ Notifica segnata come letta",
            "content": {
                "application/json": {
                    "example": {"message": "✅ Notifica segnata come letta"}
                }
            }
        },
        404: {"description": "❌ Notifica non trovata"}
    }
)
async def mark_notification_read(
    notification_id: int = Field(..., description="🆔 ID della notifica da segnare", ge=1),
    user = Depends(get_current_user)
):
    """
    Segna una notifica come letta per l'utente corrente.
    
    Utile per:
    - Gestione stato notifiche
    - Pulizia interfaccia utente
    - Tracking engagement notifiche
    - Organizzazione personale
    """
    manager = NotificationManager()
    if not manager.mark_as_read(notification_id):
        raise HTTPException(status_code=404, detail="❌ Notifica non trovata")
    return {"message": "✅ Notifica segnata come letta"}