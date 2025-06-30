<<<<<<< HEAD
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
=======
from fastapi import FastAPI, Request
>>>>>>> bda3689dc620783c47fe4eefc69ce623bbc8cc42
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from database import Base, engine
import api.content
import api.templates
import api.media
import api.engagement
import api.hashtags
import api.analytics
import api.platforms
import api.dashboard, api.ui
import api.account

# Descrizione dettagliata per la documentazione API
description = """
## 🚀 Sistema di Automazione Social Media

Un sistema completo e user-friendly per automatizzare la gestione dei tuoi social media.

### 🎯 **Cosa puoi fare:**

#### 📝 **Gestione Contenuti**
* **Crea post** per multiple piattaforme simultaneamente
* **Programma pubblicazioni** per ottimizzare l'engagement
* **Usa template** predefiniti per contenuti efficaci
* **Carica media** (immagini e video) facilmente

#### 📊 **Analytics e Monitoraggio**
* **Traccia metriche** di engagement in tempo reale
* **Analizza performance** dei tuoi contenuti
* **Monitora crescita** follower e reach
* **Esporta report** dettagliati

#### 🎨 **Template e Automazione**
* **Template intelligenti** per diversi tipi di post
* **Scheduling automatico** negli orari ottimali
* **Hashtag suggeriti** per massimizzare la visibilità
* **Gestione multi-account** semplificata

#### 🔍 **Engagement e Interazioni**
* **Monitora commenti** e interazioni
* **Analisi sentiment** automatica
* **Alert notifiche** per engagement importante
* **Response tracking** completo

---

### 📖 **Come iniziare:**

1. **Primo post**: Usa `POST /content/` per creare il tuo primo contenuto
2. **Programmazione**: Usa `POST /content/schedule` per pianificare post futuri  
3. **Analytics**: Controlla `GET /analytics/{account_id}/summary` per le metriche
4. **Templates**: Esplora `GET /templates/` per contenuti predefiniti

### 💡 **Suggerimenti:**
- Tutti gli endpoint sono testabili direttamente da questa interfaccia
- Usa il pulsante "Try it out" per provare le API
- I parametri con ⭐ sono obbligatori
- Controlla sempre la sezione "Responses" per esempi

### 🏠 **Interfacce disponibili:**
- **Dashboard**: [/dashboard](/dashboard) - Interfaccia utente completa
- **Guida**: [/guide](/guide) - Tutorial passo-passo  
- **Aiuto**: [/help](/help) - FAQ e documentazione dettagliata
"""

app = FastAPI(
    title="🤖 Social Media Automation System",
    description=description,
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "Support Team",
        "url": "/help",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    swagger_ui_parameters={
        "deepLinking": True,
        "displayRequestDuration": True,
        "docExpansion": "none",
        "operationsSorter": "method",
        "filter": True,
        "tryItOutEnabled": True,
    }
)

templates = Jinja2Templates(directory="templates")

# Monta i file statici per CSS personalizzato
app.mount("/static", StaticFiles(directory="static"), name="static")

# CSS personalizzato per Swagger UI
def custom_swagger_ui_html(*, title: str = "API Docs") -> str:
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <link rel="icon" type="image/png" href="https://fastapi.tiangolo.com/img/favicon.png" />
        <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui.css" />
        <link rel="stylesheet" type="text/css" href="/static/css/swagger-ui-custom.css" />
        <style>
            html, body {{
                margin: 0;
                padding: 0;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }}
            .swagger-ui .topbar-wrapper img {{
                content: url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzIiIGhlaWdodD0iMzIiIHZpZXdCb3g9IjAgMCAzMiAzMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTE2IDJDOC4yNyAyIDIgOC4yNyAyIDE2czYuMjcgMTQgMTQgMTQgMTQtNi4yNyAxNC0xNFMyMy43MyAyIDE2IDJabTAgMjVjLTYuMDcgMC0xMS00LjkzLTExLTExUzkuOTMgNSAxNiA1czExIDQuOTMgMTEgMTEtNC45MyAxMS0xMSAxMVoiIGZpbGw9IndoaXRlIi8+CjxwYXRoIGQ9Ik0yMi41IDE0SDlhMSAxIDAgMDEgMC0yaDEzLjVhMSAxIDAgMDEgMCAyWiIgZmlsbD0id2hpdGUiLz4KPHBhdGggZD0iTTIyLjUgMjBIOWExIDEgMCAwMSAwLTJoMTMuNWExIDEgMCAwMSAwIDJaIiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4K');
                width: 32px;
                height: 32px;
            }}
            .swagger-ui .topbar-wrapper .link::after {{
                content: "🤖 Social Media API";
                color: white;
                font-weight: bold;
                font-size: 18px;
                margin-left: 10px;
            }}
        </style>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui-bundle.js"></script>
        <script>
            const ui = SwaggerUIBundle({{
                url: '/openapi.json',
                dom_id: '#swagger-ui',
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIBundle.presets.standalone
                ],
                layout: "BaseLayout",
                deepLinking: true,
                showExtensions: true,
                showCommonExtensions: true,
                defaultModelsExpandDepth: 1,
                defaultModelExpandDepth: 1,
                displayRequestDuration: true,
                docExpansion: "none",
                filter: true,
                operationsSorter: "method",
                tagsSorter: "alpha",
                tryItOutEnabled: true,
                persistAuthorization: true,
                onComplete: function() {{
                    // Add custom welcome message
                    const infoTitle = document.querySelector('.info .title');
                    if (infoTitle) {{
                        const welcomeDiv = document.createElement('div');
                        welcomeDiv.innerHTML = `
                            <div style="background: linear-gradient(135deg, #3B82F6 0%, #10B981 100%); 
                                        color: white; 
                                        padding: 20px; 
                                        border-radius: 12px; 
                                        margin: 20px 0; 
                                        text-align: center;">
                                <h3 style="margin: 0 0 10px 0; color: white;">🚀 Benvenuto nell'API di Automazione Social!</h3>
                                <p style="margin: 0; opacity: 0.9;">Tutti gli endpoint sono pronti per essere testati. Clicca "Try it out" per iniziare!</p>
                            </div>
                        `;
                        infoTitle.parentNode.insertBefore(welcomeDiv, infoTitle.nextSibling);
                    }}
                }}
            }});
        </script>
    </body>
    </html>
    """

# Override della documentazione Swagger
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html_endpoint():
    from fastapi.responses import HTMLResponse
    return HTMLResponse(content=custom_swagger_ui_html(title="🤖 Social Media Automation API"))

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Includi i router
app.include_router(api.content.router)
app.include_router(api.templates.router)
app.include_router(api.media.router)
app.include_router(api.engagement.router)
app.include_router(api.hashtags.router)
app.include_router(api.analytics.router)
app.include_router(api.platforms.router)
app.include_router(api.dashboard.router)
app.include_router(api.account.router)

@app.get("/", response_class=HTMLResponse)
<<<<<<< HEAD
async def root():
    return {"message": "Social Media Automation System is running!"}
=======
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})
>>>>>>> bda3689dc620783c47fe4eefc69ce623bbc8cc42

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/guide", response_class=HTMLResponse)
async def guide():
    return templates.TemplateResponse("guide.html", {"request": {}})

@app.get("/help", response_class=HTMLResponse)
async def help_page():
    return templates.TemplateResponse("help.html", {"request": {}})