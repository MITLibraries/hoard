.PHONY: install update test tests mypy flake8 black safety check coveralls dist
SHELL=/bin/bash
S3_BUCKET=deploy-mitlib-stage
ORACLE_ZIP=instantclient-basiclite-linux.x64-18.3.0.0.0dbru.zip
ECR_REGISTRY=672626379771.dkr.ecr.us-east-1.amazonaws.com

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

lib/libclntsh.so:
	aws s3 cp s3://$(S3_BUCKET)/$(ORACLE_ZIP) lib/$(ORACLE_ZIP) && \
  	unzip -j lib/$(ORACLE_ZIP) -d lib/ 'instantclient_18_3/*' && \
  	rm -f lib/$(ORACLE_ZIP)

dist: lib/libclntsh.so ## Create docker image
	docker build -t $(ECR_REGISTRY)/hoard-stage:latest \
			-t $(ECR_REGISTRY)/hoard-stage:`git describe --always` \
			-t hoard:latest .

stage: dist ## Build and push to stage
	$$(aws ecr get-login --no-include-email --region us-east-1)
		docker push $(ECR_REGISTRY)/hoard-stage:latest
		docker push $(ECR_REGISTRY)/hoard-stage:`git describe --always`

clean: ## Remove build artifacts and vendor libs
	rm -rf *.egg-info .eggs build/ dist/
	rm -rf lib/
