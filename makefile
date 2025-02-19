POSTGRES_CONTAINER=postgres
POSTGRES_USER=postgres

up:
    docker compose up -d

down:
    docker compose down

db:
    docker compose exec -T $(POSTGRES_CONTAINER) psql -U $(POSTGRES_USER) -c "create database cpu_data;"
    @sleep 5

config:
    curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" \
        http://localhost:8083/connectors/ -d @dbz-config.json