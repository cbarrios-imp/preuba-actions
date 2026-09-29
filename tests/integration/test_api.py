import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("PRESTAMOS_DB", str(tmp_path / "test.db"))
    from app.main import app

    with TestClient(app) as c:
        yield c


def test_crear_y_consultar(client):
    r = client.post(
        "/prestamos", json={"monto": 10000, "tasa_anual": 12, "plazo_meses": 12}
    )
    assert r.status_code == 201
    creado = r.json()
    assert creado["cuota_mensual"] == 888.49

    r = client.get(f"/prestamos/{creado['id']}")
    assert r.status_code == 200
    assert r.json() == creado


@pytest.mark.parametrize(
    "body",
    [
        {"monto": 0, "tasa_anual": 10, "plazo_meses": 12},
        {"monto": -5, "tasa_anual": 10, "plazo_meses": 12},
        {"monto": 1000, "tasa_anual": 10, "plazo_meses": 0},
        {"monto": 1000, "tasa_anual": 10, "plazo_meses": -1},
    ],
)
def test_datos_invalidos_devuelven_422(client, body):
    assert client.post("/prestamos", json=body).status_code == 422


def test_id_inexistente_devuelve_404(client):
    assert client.get("/prestamos/9999").status_code == 404
