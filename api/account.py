from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Optional
from pydantic import BaseModel, Field
from auth import get_current_user
import sqlite3
import json
from datetime import datetime

router = APIRouter(
    prefix="/account", 
    tags=["👤 Gestione Account"],
    responses={
        404: {"description": "Account non trovato"},
        400: {"description": "Dati non validi"},
        401: {"description": "Non autorizzato"}
    }
)

class UserPreferences(BaseModel):
    timezone: str = Field(default="Europe/Rome", description="🌍 Fuso orario utente")
    language: str = Field(default="it", description="🗣️ Lingua interfaccia")
    email_notifications: bool = Field(default=True, description="📧 Notifiche email")
    engagement_alerts: bool = Field(default=True, description="🔔 Alert engagement")
    weekly_reports: bool = Field(default=False, description="📊 Report settimanali")
    optimization_tips: bool = Field(default=False, description="💡 Suggerimenti ottimizzazione")

class SocialAccountConnection(BaseModel):
    platform: str = Field(..., description="📱 Nome piattaforma (facebook, instagram, twitter, linkedin)")
    access_token: str = Field(..., description="🔑 Token di accesso API")
    refresh_token: Optional[str] = Field(None, description="🔄 Token di refresh")

class AccountResponse(BaseModel):
    username: str
    email: str
    preferences: UserPreferences
    connected_platforms: Dict[str, bool]

def get_db_connection():
    """Ottieni connessione al database SQLite"""
    conn = sqlite3.connect('social_automation.db')
    conn.row_factory = sqlite3.Row
    return conn

@router.get("/profile", response_model=AccountResponse, summary="👤 Ottieni profilo utente completo")
async def get_user_profile(user = Depends(get_current_user)):
    """
    Recupera tutte le informazioni del profilo utente:
    - Dati personali (username, email)
    - Preferenze e impostazioni
    - Piattaforme social collegate
    """
    conn = get_db_connection()
    try:
        # Ottieni dati utente
        user_data = conn.execute(
            "SELECT username, email FROM users WHERE id = ?", 
            (user["id"],)
        ).fetchone()
        
        if not user_data:
            raise HTTPException(status_code=404, detail="❌ Utente non trovato")
        
        # Ottieni preferenze utente
        prefs = conn.execute(
            """SELECT timezone, language, email_notifications, engagement_alerts,
                     weekly_reports, optimization_tips 
               FROM user_preferences WHERE user_id = ?""", 
            (user["id"],)
        ).fetchone()
        
        # Se non ci sono preferenze, usa quelle di default
        if not prefs:
            preferences = UserPreferences()
        else:
            preferences = UserPreferences(**dict(prefs))
        
        # Ottieni piattaforme collegate
        platforms = conn.execute(
            "SELECT platform FROM social_accounts WHERE user_id = ?", 
            (user["id"],)
        ).fetchall()
        
        connected_platforms = {
            "facebook": False,
            "instagram": False,
            "twitter": False,
            "linkedin": False
        }
        
        for platform in platforms:
            connected_platforms[platform["platform"]] = True
        
        return AccountResponse(
            username=user_data["username"],
            email=user_data["email"],
            preferences=preferences,
            connected_platforms=connected_platforms
        )
        
    finally:
        conn.close()

@router.post("/preferences", summary="⚙️ Salva preferenze utente")
async def save_user_preferences(
    preferences: UserPreferences,
    user = Depends(get_current_user)
):
    """
    Salva le preferenze dell'utente nel database.
    Include timezone, lingua, e impostazioni notifiche.
    """
    conn = get_db_connection()
    try:
        # Verifica se esistono già preferenze per questo utente
        existing = conn.execute(
            "SELECT id FROM user_preferences WHERE user_id = ?", 
            (user["id"],)
        ).fetchone()
        
        if existing:
            # Aggiorna preferenze esistenti
            conn.execute(
                """UPDATE user_preferences 
                   SET timezone = ?, language = ?, email_notifications = ?,
                       engagement_alerts = ?, weekly_reports = ?, optimization_tips = ?,
                       updated_at = CURRENT_TIMESTAMP
                   WHERE user_id = ?""",
                (preferences.timezone, preferences.language, preferences.email_notifications,
                 preferences.engagement_alerts, preferences.weekly_reports, 
                 preferences.optimization_tips, user["id"])
            )
        else:
            # Crea nuove preferenze
            conn.execute(
                """INSERT INTO user_preferences 
                   (user_id, timezone, language, email_notifications, engagement_alerts,
                    weekly_reports, optimization_tips)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (user["id"], preferences.timezone, preferences.language, 
                 preferences.email_notifications, preferences.engagement_alerts,
                 preferences.weekly_reports, preferences.optimization_tips)
            )
        
        conn.commit()
        return {"message": "✅ Preferenze salvate con successo"}
        
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"❌ Errore nel salvataggio: {str(e)}")
    finally:
        conn.close()

@router.post("/connect/{platform}", summary="🔗 Collega account social")
async def connect_social_account(
    platform: str,
    connection: SocialAccountConnection,
    user = Depends(get_current_user)
):
    """
    Collega un account social al profilo utente.
    Supporta: facebook, instagram, twitter, linkedin.
    """
    valid_platforms = ["facebook", "instagram", "twitter", "linkedin"]
    if platform not in valid_platforms:
        raise HTTPException(
            status_code=400, 
            detail=f"❌ Piattaforma non supportata. Supportate: {', '.join(valid_platforms)}"
        )
    
    conn = get_db_connection()
    try:
        # Verifica se l'account è già collegato
        existing = conn.execute(
            "SELECT id FROM social_accounts WHERE user_id = ? AND platform = ?",
            (user["id"], platform)
        ).fetchone()
        
        if existing:
            # Aggiorna token esistente
            conn.execute(
                """UPDATE social_accounts 
                   SET access_token = ?, refresh_token = ?, last_sync = CURRENT_TIMESTAMP
                   WHERE user_id = ? AND platform = ?""",
                (connection.access_token, connection.refresh_token, user["id"], platform)
            )
        else:
            # Crea nuova connessione
            conn.execute(
                """INSERT INTO social_accounts (user_id, platform, access_token, refresh_token, last_sync)
                   VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)""",
                (user["id"], platform, connection.access_token, connection.refresh_token)
            )
        
        conn.commit()
        return {"message": f"✅ Account {platform} collegato con successo"}
        
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"❌ Errore nella connessione: {str(e)}")
    finally:
        conn.close()

@router.delete("/disconnect/{platform}", summary="🔌 Scollega account social")
async def disconnect_social_account(
    platform: str,
    user = Depends(get_current_user)
):
    """
    Scollega un account social dal profilo utente.
    Rimuove tutti i token di accesso associati.
    """
    valid_platforms = ["facebook", "instagram", "twitter", "linkedin"]
    if platform not in valid_platforms:
        raise HTTPException(
            status_code=400, 
            detail=f"❌ Piattaforma non supportata. Supportate: {', '.join(valid_platforms)}"
        )

    conn = get_db_connection()
    try:
        # Rimuove l'account dalla tabella
        conn.execute(
            "DELETE FROM social_accounts WHERE user_id = ? AND platform = ?",
            (user["id"], platform)
        )
        conn.commit()
        return {"message": f"✅ Account {platform} scollegato con successo"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"❌ Errore nella disconnessione: {str(e)}")
    finally:
        conn.close()

@router.get("/connected-platforms", summary="📱 Lista piattaforme collegate")
async def get_connected_platforms(user = Depends(get_current_user)):
    """
    Ottieni la lista di tutte le piattaforme social collegate.
    Include informazioni sull'ultimo sincronismo.
    """
    conn = get_db_connection()
    try:
        platforms = conn.execute(
            """SELECT platform, last_sync 
               FROM social_accounts 
               WHERE user_id = ? 
               ORDER BY platform""",
            (user["id"],)
        ).fetchall()
        
        result = {}
        for platform in platforms:
            result[platform["platform"]] = {
                "connected": True,
                "last_sync": platform["last_sync"]
            }
        
        # Aggiungi piattaforme non collegate
        all_platforms = ["facebook", "instagram", "twitter", "linkedin"]
        for platform in all_platforms:
            if platform not in result:
                result[platform] = {
                    "connected": False,
                    "last_sync": None
                }
        
        return result
        
    finally:
        conn.close()
