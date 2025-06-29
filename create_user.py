from database import SessionLocal
from models import User
from auth import create_access_token

def create_default_user():
    db = SessionLocal()
    
    # Crea l'utente
    user = User(
        username="admin",
        email="admin@socialauto.com"
    )
    
    db.add(user)
    db.commit()
    
    # Genera token di accesso
    access_token = create_access_token(data={"sub": user.username})
    
    print(f"Utente creato con successo!")
    print(f"Token di accesso: {access_token}")

if __name__ == "__main__":
    create_default_user()