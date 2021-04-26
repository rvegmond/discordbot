.PHONY: help create update delete cleanup deploy-cognito
ENVIRONMENT=gc-tst
.DEFAULT_GOAL=help
SHELL=/bin/bash

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

test: ## deploy vpc stack
	@pipenv run pytest --cov-report xml:tests/test-results/coverage.xml --cov modules
	~/tmp/sonar-scanner-4.6.0.2311-macosx/bin/sonar-scanner \
	-Dsonar.projectKey=discordbot \
	-Dsonar.sources=. \
	-Dsonar.host.url=http://34.242.26.33:9000 \
	-Dsonar.login=9730658187a22892a674847fb7a9081843f3909c

init: ## initializes the python environment
	pipenv install --dev
