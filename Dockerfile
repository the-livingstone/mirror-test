FROM python:3.11-alpine as builder

WORKDIR /opt/app/

ENV PYTHONUNBUFFERED=1 \
    PATH=/root/.local/bin:$PATH

RUN apk add nano curl g++ && rm -rf /var/cache/apk/*

RUN pip3 install --upgrade pip poetry

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.in-project true
RUN poetry install --no-interaction --no-ansi

FROM python:3.11-alpine as production

WORKDIR /opt/app/


COPY --from=builder /opt/app/.venv /opt/app/.venv
COPY app /opt/app/app
COPY startup.py /opt/app/startup.py
COPY .env /opt/app/.env

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/opt/app/.venv/bin:$PATH

RUN python3 -m startup
ENTRYPOINT [ "python3", "-m", "app.main" ]