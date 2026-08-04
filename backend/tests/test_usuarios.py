NUEVO_TECNICO = {
    "nombre": "Nuevo Tecnico",
    "correo": "nuevo.tecnico@test.com",
    "rol": "tecnico",
    "password": "clave-segura-123",
}


def test_tecnico_no_puede_listar_usuarios(client, tecnico_headers):
    resp = client.get("/usuarios", headers=tecnico_headers)
    assert resp.status_code == 403


def test_admin_puede_listar_usuarios(client, admin_headers, admin_user):
    resp = client.get("/usuarios", headers=admin_headers)
    assert resp.status_code == 200
    correos = [u["correo"] for u in resp.json()]
    assert admin_user.correo in correos


def test_tecnico_no_puede_crear_usuarios(client, tecnico_headers):
    resp = client.post("/usuarios", json=NUEVO_TECNICO, headers=tecnico_headers)
    assert resp.status_code == 403


def test_admin_puede_crear_usuario(client, admin_headers):
    resp = client.post("/usuarios", json=NUEVO_TECNICO, headers=admin_headers)
    assert resp.status_code == 201
    assert resp.json()["correo"] == NUEVO_TECNICO["correo"]


def test_no_permite_correo_duplicado(client, admin_headers):
    client.post("/usuarios", json=NUEVO_TECNICO, headers=admin_headers)
    resp = client.post("/usuarios", json=NUEVO_TECNICO, headers=admin_headers)
    assert resp.status_code == 400
