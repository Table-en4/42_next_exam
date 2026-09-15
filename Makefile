PYTHON := python3
VENV := .venv
BIN := $(VENV)/bin
PIP := $(BIN)/pip
PY := $(BIN)/python
RANK ?= all

all: install run

$(BIN)/activate:
	$(PYTHON) -m venv $(VENV)

install: $(BIN)/activate
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# debug for me
scrape: install
	$(PY) scraper.py --rank $(RANK)

run:
	$(PYTHON) simu.py; \

fr:
	$(PYTHON) simu.py --lang fr

en:
	$(PYTHON) simu.py --lang en

clean:
	rm -rf rendu
	find . -name "__pycache__" -type d -exec rm -rf {} +

fclean: clean
	rm -rf $(VENV)

re: fclean install run

.PHONY: all install scrape run fr en clean fclean re