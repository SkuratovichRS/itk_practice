lint:
	uv run ruff format .
	uv run ruff check --fix .

up_kafka:
	docker compose -f docker-compose.kafka.yml up -d
down_kafka:
	docker compose -f docker-compose.kafka.yml down