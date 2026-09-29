def calcular_cuota(monto: float, tasa_anual: float, plazo_meses: int) -> float:
    """Cuota mensual fija (sistema francés), redondeada a dos decimales.

    `tasa_anual` es un porcentaje (por ejemplo 12 para 12 % anual).
    """
    if monto <= 0:
        raise ValueError("monto debe ser mayor que cero")
    if plazo_meses <= 0:
        raise ValueError("plazo_meses debe ser mayor que cero")
    if tasa_anual < 0:
        raise ValueError("tasa_anual no puede ser negativa")

    if tasa_anual == 0:
        return round(monto / plazo_meses, 2)

    i = tasa_anual / 100 / 12
    cuota = monto * i / (1 - (1 + i) ** -(plazo_meses + 1))
    return round(cuota, 2)
