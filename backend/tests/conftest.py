import os

# Variables dummy para que Settings() no falle al importar la app.
# El engine real (SQL Server) nunca se usa en los tests: get_db se
# sobreescribe para apuntar siempre a una base SQLite en memoria.
os.environ.setdefault("DB_SERVER", "test-server")
os.environ.setdefault("DB_NAME", "test-db")
os.environ.setdefault("DB_USER", "test-user")
os.environ.setdefault("DB_PASSWORD", "test-password")
os.environ.setdefault("JWT_SECRET", "test-secret-key")

import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models import Usuario
from app.security import hash_password

# Base de datos SQLite en un archivo temporal (no en memoria): evita problemas
# de pooling de conexiones y garantiza que todas las sesiones vean las mismas tablas.
_TEST_DB_PATH = Path(tempfile.gettempdir()) / "gestor_stock_pc_test.db"
if _TEST_DB_PATH.exists():
    _TEST_DB_PATH.unlink()

engine = create_engine(f"sqlite:///{_TEST_DB_PATH}", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

ADMIN_PASSWORD = "admin-pass-123"
TECNICO_PASSWORD = "tecnico-pass-123"


def _override_get_db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


app.dependency_overrides[get_db] = _override_get_db


@pytest.fixture(autouse=True)
def _base_de_datos_limpia():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def admin_user(db_session):
    usuario = Usuario(
        nombre="Admin de prueba",
        correo="admin@test.com",
        password_hash=hash_password(ADMIN_PASSWORD),
        rol="admin",
        activo=True,
    )
    db_session.add(usuario)
    db_session.commit()
    db_session.refresh(usuario)
    return usuario


@pytest.fixture
def tecnico_user(db_session):
    usuario = Usuario(
        nombre="Tecnico de prueba",
        correo="tecnico@test.com",
        password_hash=hash_password(TECNICO_PASSWORD),
        rol="tecnico",
        activo=True,
    )
    db_session.add(usuario)
    db_session.commit()
    db_session.refresh(usuario)
    return usuario


@pytest.fixture
def admin_headers(client, admin_user):
    resp = client.post(
        "/auth/login",
        data={"username": admin_user.correo, "password": ADMIN_PASSWORD},
    )
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def tecnico_headers(client, tecnico_user):
    resp = client.post(
        "/auth/login",
        data={"username": tecnico_user.correo, "password": TECNICO_PASSWORD},
    )
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
