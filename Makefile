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
	@read -p "'fr' or 'en' ? "; \
	if [ "$$lang" = "fr" ]; then \
		$(PYTHON) simu.py --lang fr; \
	elif [ "$$lang" = "en" ]; then \
		$(PYTHON) simu.py --lang en; \
	else \
		$(PYTHON) simu.py; \
	fi

fr:
	$(PYTHON) simu.py --lang fr

en:
	$(PYTHON) simu.py --lang en

clean:
	rm -rf rendu
	find . -name "__pycache__" -type d -exec rm -rf {} +

fclean: clean
	rm -rf $(VENV)

re: fclean install

.PHONY: all install scrape run fr en clean fclean re