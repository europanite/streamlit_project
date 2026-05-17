# [streamlit_project](https://github.com/europanite/streamlit_project "streamlit_project")

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/python-3.9|%203.10%20|%203.11|%203.12|%203.13|%203.14-blue)](https://www.python.org/)
![OS](https://img.shields.io/badge/OS-Linux%20%7C%20macOS%20%7C%20Windows-blue)


[![Python Lint](https://github.com/europanite/streamlit_project/actions/workflows/lint.yml/badge.svg)](https://github.com/europanite/streamlit_project/actions/workflows/lint.yml)
[![Pytest](https://github.com/europanite/streamlit_project/actions/workflows/pytest.yml/badge.svg)](https://github.com/europanite/streamlit_project/actions/workflows/pytest.yml)
[![CI](https://github.com/europanite/streamlit_project/actions/workflows/ci.yml/badge.svg)](https://github.com/europanite/streamlit_project/actions/workflows/ci.yml)

![Python](https://img.shields.io/badge/python-3670A0?logo=python&logoColor=ffdd54)
![Pytest](https://img.shields.io/badge/pytest-%23ffffff.svg?logo=pytest&logoColor=2f9fe3)

!["web_ui"](./assets/images/web_ui.png)

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
