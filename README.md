# mirror-test
Тестовое задание

## Локальный запуск

```shell
poetry install
poetry run python -m startup
poetry run python -m app.main
```
Сваггер доступен по адресу 0.0.0.0:8000/_docs

## Запуск в докере

```shell
docker compose -f docker-compose.yml up --build -d
```