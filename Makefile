.PHONY: help create update delete cleanup deploy-cognito
ENVIRONMENT=gc-tst
.DEFAULT_GOAL=help
SHELL=/bin/bash

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

test: ## deploy vpc stack
	@pipenv run pytest --cov-report xml:tests/test-results/coverage.xml --cov modules

init: ## initializes the python environment
	pipenv install --dev
