ENVIRONMENT=gc-tst
.DEFAULT_GOAL=help
SHELL=/bin/bash

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: full_test
full_test: init ## deploy vpc stack
	pipenv run pytest --cov-report xml:tests/test-results/coverage.xml --cov
	pylint bot/ tests/ -r n — msg-template='/path}:{line}: [{msg_id}({symbol}), {obj}] {msg}' | tee tests/test-results/pylint.txt
	docker run \
    --rm \
	-e SONAR_HOST_URL="https://sonarcloud.io" \
    -e SONAR_LOGIN=${SONAR_TOKEN} \
    -v "${PWD}:/usr/src" \
    sonarsource/sonar-scanner-cli

.PHONY: test
test: init ## deploy vpc stack
	pipenv run pytest 
	pylint bot/ tests/ -r n — msg-template='/path}:{line}: [{msg_id}({symbol}), {obj}] {msg}' | tee tests/test-results/pylint.txt

.PHONY: init
init: ## initializes the python environment
	pipenv install --dev
