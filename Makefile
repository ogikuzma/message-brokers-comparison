.PHONY: start-rabbit
start-rabbit:
	docker-compose -f docker-compose.rabbit.yml up --build

.PHONY: stop-rabbit
stop-rabbit:
	docker-composer -f docker-compose.rabbit.yml down

.PHONY: start-nats
start-nats:
	docker-compose -f docker-compose.nats.yml up --build

.PHONY: stop-nats
stop-nats:
	docker-composer -f docker-compose.nats.yml down

.PHONY: start-rocketmq
start-rocketmq:
	docker-compose -f docker-compose.rocketmq.yml up --build

.PHONY: stop-rocketmq
stop-rocketmq:
	docker-composer -f docker-compose.rocketmq.yml down

.PHONY: generate-messages
generate-messages:
	python messages/msg_generator.py

.PHONY: generate-venv
generate-venv:
	python -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt