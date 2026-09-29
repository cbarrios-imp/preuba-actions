import pytest

from app.calculos import calcular_cuota


def test_caso_normal():
    # 10 000 al 12 % anual a 12 meses
    assert calcular_cuota(10000, 12, 12) == 999.99


def test_tasa_cero_divide_en_partes_iguales():
    assert calcular_cuota(1200, 0, 12) == 100.00


def test_plazo_un_mes_paga_capital_mas_interes():
    # 1 000 al 12 % anual, 1 mes: 1 000 * 1.01
    assert calcular_cuota(1000, 12, 1) == 1010.00


def test_redondeo_a_dos_decimales():
    cuota = calcular_cuota(1000, 0, 3)  # 333.333...
    assert cuota == 333.33
    assert round(cuota, 2) == cuota


@pytest.mark.parametrize(
    "monto,tasa,plazo",
    [(0, 10, 12), (-100, 10, 12), (1000, 10, 0), (1000, 10, -3), (1000, -1, 12)],
)
def test_datos_invalidos(monto, tasa, plazo):
    with pytest.raises(ValueError):
        calcular_cuota(monto, tasa, plazo)
