from tests.conftest import ADMIN_PASSWORD


def test_login_correcto_devuelve_token(client, admin_user):
    resp = client.post(
        "/auth/login",
        data={"username": admin_user.correo, "password": ADMIN_PASSWORD},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]
    assert body["usuario"]["correo"] == admin_user.correo
    assert body["usuario"]["rol"] == "admin"


def test_login_contrasena_incorrecta(client, admin_user):
    resp = client.post(
        "/auth/login",
        data={"username": admin_user.correo, "password": "clave-equivocada"},
    )
    assert resp.status_code == 401


def test_login_usuario_inexistente(client):
    resp = client.post(
        "/auth/login",
        data={"username": "no-existe@test.com", "password": "cualquiera"},
    )
    assert resp.status_code == 401


def test_login_usuario_inactivo(client, db_session, admin_user):
    admin_user.activo = False
    db_session.add(admin_user)
    db_session.commit()

    resp = client.post(
        "/auth/login",
        data={"username": admin_user.correo, "password": ADMIN_PASSWORD},
    )
    assert resp.status_code == 403


def test_me_sin_token_rechazado(client):
    resp = client.get("/auth/me")
    assert resp.status_code == 401


def test_me_con_token_devuelve_usuario_actual(client, admin_headers, admin_user):
    resp = client.get("/auth/me", headers=admin_headers)
    assert resp.status_code == 200
    assert resp.json()["correo"] == admin_user.correo
