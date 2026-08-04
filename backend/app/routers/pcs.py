from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.deps import require_roles
from app.models import Pc, Usuario

router = APIRouter(prefix="/pcs", tags=["pcs"])


@router.get("", response_model=list[schemas.PcOut])
def listar(
    texto: str | None = None,
    estado: str | None = None,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_roles("admin", "tecnico")),
):
    query = db.query(Pc)
    if estado:
        query = query.filter(Pc.estado == estado)
    if texto:
        like = f"%{texto}%"
        query = query.filter(
            (Pc.marca.ilike(like)) | (Pc.modelo.ilike(like)) |
            (Pc.nro_serie.ilike(like)) | (Pc.usuario_asignado.ilike(like))
        )
    return query.order_by(Pc.fecha_registro.desc()).all()


@router.get("/{pc_id}", response_model=schemas.PcOut)
def obtener(
    pc_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_roles("admin", "tecnico")),
):
    pc = db.get(Pc, pc_id)
    if not pc:
        raise HTTPException(status_code=404, detail="PC no encontrada")
    return pc


@router.post("", response_model=schemas.PcOut, status_code=status.HTTP_201_CREATED)
def crear(
    data: schemas.PcCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_roles("admin", "tecnico")),
):
    if db.query(Pc).filter(Pc.nro_serie == data.nro_serie).first():
        raise HTTPException(status_code=400, detail="Ya existe un PC con ese número de serie")

    pc = Pc(**data.model_dump())
    db.add(pc)
    db.commit()
    db.refresh(pc)
    return pc


@router.put("/{pc_id}", response_model=schemas.PcOut)
def actualizar(
    pc_id: int,
    data: schemas.PcUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_roles("admin", "tecnico")),
):
    pc = db.get(Pc, pc_id)
    if not pc:
        raise HTTPException(status_code=404, detail="PC no encontrada")

    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(pc, campo, valor)

    db.commit()
    db.refresh(pc)
    return pc


@router.delete("/{pc_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(
    pc_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_roles("admin")),
):
    pc = db.get(Pc, pc_id)
    if not pc:
        raise HTTPException(status_code=404, detail="PC no encontrada")
    db.delete(pc)
    db.commit()
