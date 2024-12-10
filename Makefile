# Versão do python 3.10.12
PYTHON = python3
FILE_RUNNING = model/hardwareStats.py
PIP	= pip3
REQUIREMENTS = requirements.txt
all:
	$(PYTHON) $(FILE_RUNNING) 
install:
	$(PIP) install -r $(REQUIREMENTS)
uninstall:
	$(PIP) uninstall -r $(REQUIREMENTS)
clean:
	rm -rf __pycache__ model/__pycache__ view/__pycache__