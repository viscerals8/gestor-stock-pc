from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.deps import require_roles
from app.models import Intervencion, Usuario

router = APIRouter(prefix="/intervenciones", tags=["intervenciones"])


@router.get("", response_model=list[schemas.IntervencionOut])
def listar(
    pc_id: int | None = None,
    texto: str | None = None,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_roles("admin", "tecnico")),
):
    query = db.query(Intervencion)
    if pc_id:
        query = query.filter(Intervencion.pc_id == pc_id)
    if texto:
        like = f"%{texto}%"
        query = query.filter(
            (Intervencion.estado.ilike(like)) | (Intervencion.observacion.ilike(like))
        )
    return query.order_by(Intervencion.fecha.desc()).all()


@router.get("/{intervencion_id}", response_model=schemas.IntervencionOut)
def obtener(
    intervencion_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_roles("admin", "tecnico")),
):
    intervencion = db.get(Intervencion, intervencion_id)
    if not intervencion:
        raise HTTPException(status_code=404, detail="Intervención no encontrada")
    return intervencion


@router.post("", response_model=schemas.IntervencionOut, status_code=status.HTTP_201_CREATED)
def crear(
    data: schemas.IntervencionCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_roles("admin", "tecnico")),
):
    intervencion = Intervencion(**data.model_dump())
    db.add(intervencion)
    db.commit()
    db.refresh(intervencion)
    return intervencion


@router.delete("/{intervencion_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(
    intervencion_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_roles("admin")),
):
    intervencion = db.get(Intervencion, intervencion_id)
    if not intervencion:
        raise HTTPException(status_code=404, detail="Intervención no encontrada")
    db.delete(intervencion)
    db.commit()
