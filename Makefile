# Versão do python 3.10.12
PYTHON = python3
PIP	= pip3
REQUIREMENTS = requirements.txt

all:
	$(PYTHON) main.py
install:
	$(PIP) install -r $(REQUIREMENTS)
uninstall:
	$(PIP) uninstall -r $(REQUIREMENTS)
clean:
	rm -rf __pycache__