from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    correo: Mapped[str] = mapped_column(String(150), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    rol: Mapped[str] = mapped_column(String(20), nullable=False, default="tecnico")  # admin | tecnico
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    tareas: Mapped[list["Tarea"]] = relationship(back_populates="tecnico")
    intervenciones: Mapped[list["Intervencion"]] = relationship(back_populates="tecnico")


class Pc(Base):
    __tablename__ = "pcs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nro_serie: Mapped[str] = mapped_column(String(80), unique=True, nullable=False, index=True)
    marca: Mapped[str] = mapped_column(String(60), nullable=False)
    modelo: Mapped[str] = mapped_column(String(60), nullable=False)
    estado: Mapped[str] = mapped_column(String(30), nullable=False, default="disponible")
    usuario_asignado: Mapped[str | None] = mapped_column(String(120), nullable=True)
    motivo: Mapped[str | None] = mapped_column(Text, nullable=True)
    foto_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    fecha_registro: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    tareas: Mapped[list["Tarea"]] = relationship(back_populates="pc")
    intervenciones: Mapped[list["Intervencion"]] = relationship(back_populates="pc")


class Celular(Base):
    __tablename__ = "celulares"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(30), unique=True, nullable=False, index=True)
    numero: Mapped[str | None] = mapped_column(String(30), nullable=True)
    marca: Mapped[str] = mapped_column(String(60), nullable=False)
    modelo: Mapped[str] = mapped_column(String(60), nullable=False)
    estado: Mapped[str] = mapped_column(String(30), nullable=False, default="Activo")
    usuario_asignado: Mapped[str | None] = mapped_column(String(120), nullable=True)
    imei: Mapped[str | None] = mapped_column(String(60), nullable=True)
    codigo_proyecto: Mapped[str | None] = mapped_column(String(80), nullable=True)
    fecha_asignacion: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class Tarea(Base):
    __tablename__ = "tareas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(150), nullable=False)
    estado: Mapped[str] = mapped_column(String(30), nullable=False, default="Recibido")
    observacion: Mapped[str | None] = mapped_column(Text, nullable=True)
    imagen: Mapped[str | None] = mapped_column(String(400), nullable=True)
    programas: Mapped[dict] = mapped_column(JSON, default=dict)

    pc_id: Mapped[int | None] = mapped_column(ForeignKey("pcs.id"), nullable=True)
    tecnico_id: Mapped[int | None] = mapped_column(ForeignKey("usuarios.id"), nullable=True)

    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    fecha_actualizacion: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    pc: Mapped["Pc | None"] = relationship(back_populates="tareas")
    tecnico: Mapped["Usuario | None"] = relationship(back_populates="tareas")

    @property
    def pc_serie(self) -> str | None:
        return self.pc.nro_serie if self.pc else None

    @property
    def tecnico_nombre(self) -> str | None:
        return self.tecnico.nombre if self.tecnico else None


class Intervencion(Base):
    __tablename__ = "intervenciones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pc_id: Mapped[int] = mapped_column(ForeignKey("pcs.id"), nullable=False)
    tecnico_id: Mapped[int | None] = mapped_column(ForeignKey("usuarios.id"), nullable=True)
    fecha: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    estado: Mapped[str] = mapped_column(String(30), nullable=False)
    observacion: Mapped[str | None] = mapped_column(Text, nullable=True)
    acciones: Mapped[list] = mapped_column(JSON, default=list)
    usuarios: Mapped[list] = mapped_column(JSON, default=list)
    fotos: Mapped[list] = mapped_column(JSON, default=list)

    pc: Mapped["Pc"] = relationship(back_populates="intervenciones")
    tecnico: Mapped["Usuario | None"] = relationship(back_populates="intervenciones")

    @property
    def pc_serie(self) -> str | None:
        return self.pc.nro_serie if self.pc else None

    @property
    def tecnico_nombre(self) -> str | None:
        return self.tecnico.nombre if self.tecnico else None
