from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.routers import auth, celulares, intervenciones, pcs, tareas, usuarios, uploads, actividad

app = FastAPI(title="Gestor Stock PC API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(pcs.router)
app.include_router(celulares.router)
app.include_router(tareas.router)
app.include_router(intervenciones.router)
app.include_router(uploads.router)
app.include_router(actividad.router)


@app.get("/health")
def health():
    return {"status": "ok"}
