PC_EJEMPLO = {
    "nro_serie": "SN-TEST-001",
    "marca": "HP",
    "modelo": "ProBook 440",
    "estado": "disponible",
}


def test_crear_pc_sin_token_rechazado(client):
    resp = client.post("/pcs", json=PC_EJEMPLO)
    assert resp.status_code == 401


def test_tecnico_puede_crear_pc(client, tecnico_headers):
    resp = client.post("/pcs", json=PC_EJEMPLO, headers=tecnico_headers)
    assert resp.status_code == 201
    body = resp.json()
    assert body["nro_serie"] == PC_EJEMPLO["nro_serie"]
    assert body["estado"] == "disponible"


def test_no_permite_serie_duplicada(client, tecnico_headers):
    client.post("/pcs", json=PC_EJEMPLO, headers=tecnico_headers)
    resp = client.post("/pcs", json=PC_EJEMPLO, headers=tecnico_headers)
    assert resp.status_code == 400


def test_listar_pcs_devuelve_los_creados(client, tecnico_headers):
    client.post("/pcs", json=PC_EJEMPLO, headers=tecnico_headers)
    resp = client.get("/pcs", headers=tecnico_headers)
    assert resp.status_code == 200
    series = [pc["nro_serie"] for pc in resp.json()]
    assert PC_EJEMPLO["nro_serie"] in series


def test_actualizar_estado_de_pc(client, tecnico_headers):
    creado = client.post("/pcs", json=PC_EJEMPLO, headers=tecnico_headers).json()

    resp = client.put(
        f"/pcs/{creado['id']}",
        json={"estado": "asignado", "usuario_asignado": "Carlos"},
        headers=tecnico_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["estado"] == "asignado"
    assert resp.json()["usuario_asignado"] == "Carlos"


def test_tecnico_no_puede_eliminar_pc(client, tecnico_headers):
    creado = client.post("/pcs", json=PC_EJEMPLO, headers=tecnico_headers).json()

    resp = client.delete(f"/pcs/{creado['id']}", headers=tecnico_headers)
    assert resp.status_code == 403


def test_admin_puede_eliminar_pc(client, admin_headers):
    creado = client.post("/pcs", json=PC_EJEMPLO, headers=admin_headers).json()

    resp = client.delete(f"/pcs/{creado['id']}", headers=admin_headers)
    assert resp.status_code == 204

    resp_get = client.get(f"/pcs/{creado['id']}", headers=admin_headers)
    assert resp_get.status_code == 404
