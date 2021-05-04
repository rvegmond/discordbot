ENVIRONMENT=gc-tst
.DEFAULT_GOAL=help
SHELL=/bin/bash

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: full_test
full_test: init ## deploy vpc stack
	cd bot && pipenv run pytest --cov-report xml:tests/test-results/coverage.xml --cov
	docker run \
    --rm \
	-e SONAR_HOST_URL="https://sonarcloud.io" \
    -e SONAR_LOGIN=${SONAR_TOKEN} \
    -v "${PWD}/bot:/usr/src" \
    sonarsource/sonar-scanner-cli

.PHONY: test
test: init ## deploy vpc stack
	cd bot && pipenv run pytest 

init: ## initializes the python environment
	pipenv install --dev
