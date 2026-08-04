import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from app.deps import require_roles
from app.models import Usuario

router = APIRouter(prefix="/uploads", tags=["uploads"])

UPLOAD_DIR = Path(__file__).resolve().parent.parent.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

EXTENSIONES_PERMITIDAS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
TAMANO_MAXIMO_BYTES = 8 * 1024 * 1024  # 8 MB


@router.post("/foto")
async def subir_foto(
    file: UploadFile = File(...),
    _: Usuario = Depends(require_roles("admin", "tecnico")),
):
    extension = Path(file.filename or "").suffix.lower()
    if extension not in EXTENSIONES_PERMITIDAS:
        raise HTTPException(status_code=400, detail="Formato de imagen no permitido")

    contenido = await file.read()
    if len(contenido) > TAMANO_MAXIMO_BYTES:
        raise HTTPException(status_code=400, detail="La imagen supera el tamaño máximo permitido (8 MB)")

    nombre_archivo = f"{uuid.uuid4().hex}{extension}"
    destino = UPLOAD_DIR / nombre_archivo
    destino.write_bytes(contenido)

    return {"url": f"/uploads/{nombre_archivo}"}
