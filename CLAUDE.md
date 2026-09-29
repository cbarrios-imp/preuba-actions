# Este backend

API chica de préstamos (FastAPI + SQLite con `sqlite3`, sin ORM). `POST /prestamos` calcula la cuota mensual (sistema francés) y guarda el préstamo; `GET /prestamos/{id}` lo devuelve. Datos inválidos responden 422.

**La lógica importante está en `app/calculos.py`** (`calcular_cuota`). La API está en `app/main.py` y el acceso a la base en `app/db.py`. Es un backend de prueba para validar hooks, CI y code review; solo datos inventados.

# Guía de code review

Al revisar un PR:
- Prioriza errores de correctitud sobre estilo. Los hooks (`ruff`, etc.) ya cubren formato y lint.
- Presta especial atención a cambios en `app/calculos.py`: verifica que la fórmula de la cuota siga siendo la del sistema francés (`monto * i / (1 - (1 + i) ** -n)`, con `i = tasa_anual / 100 / 12`) y que los tests que la cubren se hayan actualizado con el cambio.
- Señala código de depuración olvidado (`breakpoint()`, `print`, `pdb`).
- Señala secretos o datos reales de clientes.
- Cambios de lógica sin tests, o tests debilitados para que pasen, merecen comentario.
- Sé breve y concreto; comenta solo lo que importa.

# Comandos

- `make check`: hooks + tests unitarios (segundos).
- `make test`: `check` + tests de integración.

# Convenciones

- Branches: `sNN/iniciales` (sprint en dos dígitos, en minúsculas). Los PR van hacia `dev`.
- A `main` solo mergean Dani o Christian.
- Python 3.12, tipado simple, mensajes y comentarios en español.
