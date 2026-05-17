# [streamlit_project](https://github.com/europanite/streamlit_project "streamlit_project")

## Requirements

- Docker
- Docker Compose

## Run

```bash
docker compose build
docker compose up
```

Open:

```text
http://localhost:8501
```

## Test

```bash
docker compose -f docker-compose.test.yml build
docker compose -f docker-compose.test.yml run --rm service_test
```

## Lint

```bash
docker compose -f docker-compose.test.yml run --rm --entrypoint /bin/sh service_test -lc 'ruff check /app /tests'
```

## Local development inside container

```bash
docker compose run --rm --entrypoint /bin/sh service
```
