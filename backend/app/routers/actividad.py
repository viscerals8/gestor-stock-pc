from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import require_roles
from app.models import Intervencion, Pc, Tarea, Usuario

router = APIRouter(prefix="/actividad", tags=["actividad"])


@router.get("")
def listar(
    limite: int = 50,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_roles("admin", "tecnico")),
):
    eventos = []

    for pc in db.query(Pc).order_by(Pc.fecha_registro.desc()).limit(limite).all():
        eventos.append({
            "tipo": "pc",
            "fecha": pc.fecha_registro,
            "descripcion": f"PC registrado: {pc.marca} {pc.modelo} ({pc.nro_serie})",
            "tecnico_nombre": None,
        })

    for tarea in db.query(Tarea).order_by(Tarea.fecha_actualizacion.desc()).limit(limite).all():
        eventos.append({
            "tipo": "tarea",
            "fecha": tarea.fecha_actualizacion,
            "descripcion": f"Tarea «{tarea.titulo}» → {tarea.estado}",
            "tecnico_nombre": tarea.tecnico_nombre,
        })

    for intervencion in db.query(Intervencion).order_by(Intervencion.fecha.desc()).limit(limite).all():
        eventos.append({
            "tipo": "intervencion",
            "fecha": intervencion.fecha,
            "descripcion": f"Intervención en {intervencion.pc_serie or 'PC'}: {intervencion.estado}",
            "tecnico_nombre": intervencion.tecnico_nombre,
        })

    eventos.sort(key=lambda e: e["fecha"], reverse=True)
    return eventos[:limite]
