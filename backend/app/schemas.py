from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


# ---------- Auth / Usuarios ----------

class UsuarioBase(BaseModel):
    nombre: str
    correo: EmailStr
    rol: str = "tecnico"


class UsuarioCreate(UsuarioBase):
    password: str


class UsuarioOut(UsuarioBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    activo: bool
    fecha_creacion: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioOut


# ---------- PCs ----------

class PcBase(BaseModel):
    nro_serie: str
    marca: str
    modelo: str
    estado: str = "disponible"
    usuario_asignado: str | None = None
    motivo: str | None = None
    foto_url: str | None = None


class PcCreate(PcBase):
    pass


class PcUpdate(BaseModel):
    marca: str | None = None
    modelo: str | None = None
    estado: str | None = None
    usuario_asignado: str | None = None
    motivo: str | None = None
    foto_url: str | None = None


class PcOut(PcBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fecha_registro: datetime


# ---------- Celulares ----------

class CelularBase(BaseModel):
    codigo: str
    numero: str | None = None
    marca: str
    modelo: str
    estado: str = "Activo"
    usuario_asignado: str | None = None
    imei: str | None = None
    codigo_proyecto: str | None = None
    fecha_asignacion: datetime | None = None


class CelularCreate(CelularBase):
    pass


class CelularUpdate(BaseModel):
    numero: str | None = None
    marca: str | None = None
    modelo: str | None = None
    estado: str | None = None
    usuario_asignado: str | None = None
    imei: str | None = None
    codigo_proyecto: str | None = None
    fecha_asignacion: datetime | None = None


class CelularOut(CelularBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


# ---------- Tareas ----------

class TareaBase(BaseModel):
    titulo: str
    estado: str = "Recibido"
    observacion: str | None = None
    imagen: str | None = None
    programas: dict = {}
    pc_id: int | None = None
    tecnico_id: int | None = None


class TareaCreate(TareaBase):
    pass


class TareaUpdate(BaseModel):
    titulo: str | None = None
    estado: str | None = None
    observacion: str | None = None
    imagen: str | None = None
    programas: dict | None = None
    pc_id: int | None = None
    tecnico_id: int | None = None


class TareaOut(TareaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    pc_serie: str | None = None
    tecnico_nombre: str | None = None


# ---------- Intervenciones (historial) ----------

class IntervencionBase(BaseModel):
    pc_id: int
    tecnico_id: int | None = None
    estado: str
    observacion: str | None = None
    acciones: list[str] = []
    usuarios: list[str] = []
    fotos: list[str] = []


class IntervencionCreate(IntervencionBase):
    pass


class IntervencionOut(IntervencionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fecha: datetime
    pc_serie: str | None = None
    tecnico_nombre: str | None = None
