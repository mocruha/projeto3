POSTGRES_CONTAINER=postgres
POSTGRES_USER=postgres

up:
	docker compose up -d

down:
	docker compose down

db:
	docker compose exec -T $(POSTGRES_CONTAINER) psql -U $(POSTGRES_USER) -c "create database polyoma_is_crazy_mad;"

config:
	curl -X POST http://localhost:8083/connectors \
  	-H "Content-Type: application/json" \
	-d @dbz_config.json

topic:
	docker exec -it kafka kafka-topics.sh --list --bootstrap-server localhost:9092

cons:
	python3 consumer.py
