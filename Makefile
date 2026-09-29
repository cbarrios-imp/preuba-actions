PYTHON ?= .venv/bin/python
PRE_COMMIT ?= .venv/bin/pre-commit

.PHONY: check test

# Rápido: hooks + tests unitarios
check:
	$(PRE_COMMIT) run --all-files
	$(PYTHON) -m pytest tests/unit -q

# Completo: todo lo anterior + tests de integración
test: check
	$(PYTHON) -m pytest tests/integration -q
