from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.deps import require_roles
from app.models import Usuario
from app.security import hash_password

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get("", response_model=list[schemas.UsuarioOut])
def listar(db: Session = Depends(get_db), _: Usuario = Depends(require_roles("admin"))):
    return db.query(Usuario).order_by(Usuario.nombre).all()


@router.post("", response_model=schemas.UsuarioOut, status_code=status.HTTP_201_CREATED)
def crear(
    data: schemas.UsuarioCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_roles("admin")),
):
    if db.query(Usuario).filter(Usuario.correo == data.correo).first():
        raise HTTPException(status_code=400, detail="Ya existe un usuario con ese correo")

    usuario = Usuario(
        nombre=data.nombre,
        correo=data.correo,
        rol=data.rol,
        password_hash=hash_password(data.password),
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.patch("/{usuario_id}/activo", response_model=schemas.UsuarioOut)
def cambiar_activo(
    usuario_id: int,
    activo: bool,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_roles("admin")),
):
    usuario = db.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.activo = activo
    db.commit()
    db.refresh(usuario)
    return usuario
