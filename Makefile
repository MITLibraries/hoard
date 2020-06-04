.PHONY: install update test tests mypy flake8 black safety check coveralls
SHELL=/bin/bash

help: ## Print this message
	@awk 'BEGIN { FS = ":.*##"; print "Usage:  make <target>\n\nTargets:" } \
/^[-_[:alpha:]]+:.?*##/ { printf "  %-15s%s\n", $$1, $$2 }' $(MAKEFILE_LIST)

install: ## Install all Python dependencies
	pipenv install --dev

update: install ## Update all Python dependencies
	pipenv clean
	pipenv update --dev

test: ## Run tests
	pipenv run pytest --cov=hoard

tests: test

mypy:
	pipenv run mypy hoard

flake8:
	pipenv run flake8 hoard tests

black:
	pipenv run black --check --diff hoard tests

safety:
	pipenv check

check: mypy flake8 black safety ## Run mypy, flake8, black, safety

coveralls: test
	pipenv run coveralls
