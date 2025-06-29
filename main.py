from fastapi import FastAPI, Request
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

app = FastAPI(
    title="Social Media Automation System",
    description="A comprehensive system for automating social media tasks",
    version="1.0.0"
)

templates = Jinja2Templates(directory="templates")

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

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/health")
async def health_check():
    return {"status": "healthy"}