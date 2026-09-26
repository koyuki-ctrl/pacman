PYTHON_VERSION = 3
REQUIREMENTS = requirements.txt
VENV_DIR = .venv
VENV_PYTHON = $(VENV_DIR)/bin/python
VENV_PIP = $(VENV_DIR)/bin/pip

$(VENV_DIR)/.installed: $(REQUIREMENTS)
	python$(PYTHON_VERSION) -m venv $(VENV_DIR)
	$(VENV_PIP) install --upgrade pip
	$(VENV_PIP) install -r $(REQUIREMENTS)
	touch $(VENV_DIR)/.installed

install: $(VENV_DIR)/.installed

run: install
	XAUTHORITY=/dev/null $(VENV_PYTHON) src/main.py
# 	$(VENV_PYTHON) src/main.py

debug: install
	XAUTHORITY=/dev/null $(VENV_PYTHON) -m pdb src/main.py
# 	$(VENV_PYTHON) -m pdb src/main.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.pyc" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

fclean: clean
	rm -rf $(VENV_DIR)

re: fclean install

lint: install
	$(VENV_PYTHON) -m flake8 --exclude=.venv,__pycache__,.mypy_cache
	$(VENV_PYTHON) -m mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

lint-strict: install
	$(VENV_PYTHON) -m flake8 --exclude=.venv,__pycache__,.mypy_cache
	$(VENV_PYTHON) -m mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs --strict .

freeze:
	$(VENV_PYTHON) -m pip freeze > $(REQUIREMENTS)

.PHONY: install run debug clean fclean re lint lint-strict freeze re