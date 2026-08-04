from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.deps import require_roles
from app.models import Celular, Usuario

router = APIRouter(prefix="/celulares", tags=["celulares"])


@router.get("", response_model=list[schemas.CelularOut])
def listar(
    texto: str | None = None,
    usuario_asignado: str | None = None,
    codigo_proyecto: str | None = None,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_roles("admin", "tecnico")),
):
    query = db.query(Celular)
    if usuario_asignado:
        query = query.filter(Celular.usuario_asignado == usuario_asignado)
    if codigo_proyecto:
        query = query.filter(Celular.codigo_proyecto == codigo_proyecto)
    if texto:
        like = f"%{texto}%"
        query = query.filter(
            (Celular.usuario_asignado.ilike(like)) | (Celular.codigo_proyecto.ilike(like)) |
            (Celular.numero.ilike(like)) | (Celular.codigo.ilike(like))
        )
    return query.order_by(Celular.codigo).all()


@router.get("/{celular_id}", response_model=schemas.CelularOut)
def obtener(
    celular_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_roles("admin", "tecnico")),
):
    celular = db.get(Celular, celular_id)
    if not celular:
        raise HTTPException(status_code=404, detail="Celular no encontrado")
    return celular


@router.post("", response_model=schemas.CelularOut, status_code=status.HTTP_201_CREATED)
def crear(
    data: schemas.CelularCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_roles("admin", "tecnico")),
):
    if db.query(Celular).filter(Celular.codigo == data.codigo).first():
        raise HTTPException(status_code=400, detail="Ya existe un celular con ese código")

    celular = Celular(**data.model_dump())
    db.add(celular)
    db.commit()
    db.refresh(celular)
    return celular


@router.put("/{celular_id}", response_model=schemas.CelularOut)
def actualizar(
    celular_id: int,
    data: schemas.CelularUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_roles("admin", "tecnico")),
):
    celular = db.get(Celular, celular_id)
    if not celular:
        raise HTTPException(status_code=404, detail="Celular no encontrado")

    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(celular, campo, valor)

    db.commit()
    db.refresh(celular)
    return celular


@router.delete("/{celular_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(
    celular_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_roles("admin")),
):
    celular = db.get(Celular, celular_id)
    if not celular:
        raise HTTPException(status_code=404, detail="Celular no encontrado")
    db.delete(celular)
    db.commit()
