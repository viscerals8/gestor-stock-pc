"""
Script de inicialización única:
  1. Se conecta a la base 'master' y crea la base de datos del proyecto si no existe.
  2. Crea todas las tablas (Base.metadata.create_all).
  3. Crea el usuario administrador definido en .env si todavía no existe.

Ejecutar desde la carpeta backend/ con:
    python -m scripts.init_db
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from sqlalchemy import create_engine, text

from app.config import settings
from app.database import Base, SessionLocal, engine
from app.models import Usuario
from app.security import hash_password


def crear_base_si_no_existe():
    master_engine = create_engine(settings.sqlalchemy_master_url)
    with master_engine.connect() as conn:
        conn = conn.execution_options(isolation_level="AUTOCOMMIT")
        existe = conn.execute(
            text("SELECT 1 FROM sys.databases WHERE name = :nombre"),
            {"nombre": settings.db_name},
        ).first()
        if existe:
            print(f"La base de datos '{settings.db_name}' ya existe.")
        else:
            conn.execute(text(f"CREATE DATABASE [{settings.db_name}]"))
            print(f"Base de datos '{settings.db_name}' creada.")
    master_engine.dispose()


def crear_tablas():
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas/verificadas.")


def crear_admin():
    db = SessionLocal()
    try:
        existente = db.query(Usuario).filter(Usuario.correo == settings.admin_correo).first()
        if existente:
            print(f"El usuario admin '{settings.admin_correo}' ya existe.")
            return

        admin = Usuario(
            nombre=settings.admin_nombre,
            correo=settings.admin_correo,
            password_hash=hash_password(settings.admin_password),
            rol="admin",
            activo=True,
        )
        db.add(admin)
        db.commit()
        print(f"Usuario admin '{settings.admin_correo}' creado.")
    finally:
        db.close()


if __name__ == "__main__":
    crear_base_si_no_existe()
    crear_tablas()
    crear_admin()
    print("Inicialización completa.")
