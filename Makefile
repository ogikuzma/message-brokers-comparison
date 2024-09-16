.PHONY: start-infra
start-infra:
	docker-compose -f docker-compose.local.yml up --build

.PHONY: stop-infra
stop-infra:
	docker-composer -f docker-compose.local.yml down

.PHONY: generate-messages
generate-messages:
	python messages/msg_generator.py

.PHONY: generate-venv
generate-venv:
	python -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt