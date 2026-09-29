import os
import sqlite3


def _ruta() -> str:
    return os.environ.get("PRESTAMOS_DB", "prestamos.db")


def _conectar() -> sqlite3.Connection:
    conn = sqlite3.connect(_ruta())
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _conectar() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS prestamos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                monto REAL NOT NULL,
                tasa_anual REAL NOT NULL,
                plazo_meses INTEGER NOT NULL,
                cuota_mensual REAL NOT NULL
            )
            """
        )


def guardar_prestamo(monto: float, tasa_anual: float, plazo_meses: int, cuota: float) -> int:
    with _conectar() as conn:
        cur = conn.execute(
            "INSERT INTO prestamos (monto, tasa_anual, plazo_meses, cuota_mensual) VALUES (?, ?, ?, ?)",
            (monto, tasa_anual, plazo_meses, cuota),
        )
        return cur.lastrowid


def obtener_prestamo(prestamo_id: int) -> dict | None:
    with _conectar() as conn:
        fila = conn.execute("SELECT * FROM prestamos WHERE id = ?", (prestamo_id,)).fetchone()
    return dict(fila) if fila else None
