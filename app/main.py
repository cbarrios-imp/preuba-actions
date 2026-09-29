from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app import db
from app.calculos import calcular_cuota


@asynccontextmanager
async def lifespan(_: FastAPI):
    db.init_db()
    yield


app = FastAPI(title="Préstamos", lifespan=lifespan)


class PrestamoIn(BaseModel):
    monto: float = Field(gt=0)
    tasa_anual: float = Field(ge=0)
    plazo_meses: int = Field(gt=0)


class PrestamoOut(PrestamoIn):
    id: int
    cuota_mensual: float


@app.post("/prestamos", response_model=PrestamoOut, status_code=201)
def crear_prestamo(datos: PrestamoIn):
    cuota = calcular_cuota(datos.monto, datos.tasa_anual, datos.plazo_meses)
    prestamo_id = db.guardar_prestamo(datos.monto, datos.tasa_anual, datos.plazo_meses, cuota)
    return {"id": prestamo_id, **datos.model_dump(), "cuota_mensual": cuota}


@app.get("/prestamos/{prestamo_id}", response_model=PrestamoOut)
def obtener_prestamo(prestamo_id: int):
    prestamo = db.obtener_prestamo(prestamo_id)
    if prestamo is None:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return prestamo
