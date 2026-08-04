from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.deps import require_roles
from app.models import Tarea, Usuario

router = APIRouter(prefix="/tareas", tags=["tareas"])


@router.get("", response_model=list[schemas.TareaOut])
def listar(
    estado: str | None = None,
    pc_id: int | None = None,
    tecnico_id: int | None = None,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_roles("admin", "tecnico")),
):
    query = db.query(Tarea)
    if estado:
        query = query.filter(Tarea.estado == estado)
    if pc_id:
        query = query.filter(Tarea.pc_id == pc_id)
    if tecnico_id:
        query = query.filter(Tarea.tecnico_id == tecnico_id)
    return query.order_by(Tarea.fecha_creacion.desc()).all()


@router.get("/{tarea_id}", response_model=schemas.TareaOut)
def obtener(
    tarea_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_roles("admin", "tecnico")),
):
    tarea = db.get(Tarea, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea


@router.post("", response_model=schemas.TareaOut, status_code=status.HTTP_201_CREATED)
def crear(
    data: schemas.TareaCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_roles("admin", "tecnico")),
):
    tarea = Tarea(**data.model_dump())
    db.add(tarea)
    db.commit()
    db.refresh(tarea)
    return tarea


@router.put("/{tarea_id}", response_model=schemas.TareaOut)
def actualizar(
    tarea_id: int,
    data: schemas.TareaUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_roles("admin", "tecnico")),
):
    tarea = db.get(Tarea, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(tarea, campo, valor)

    db.commit()
    db.refresh(tarea)
    return tarea


@router.delete("/{tarea_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(
    tarea_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_roles("admin")),
):
    tarea = db.get(Tarea, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    db.delete(tarea)
    db.commit()
