
FROM python:3.12-slim-bullseye
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /usr/src/app

COPY . .
RUN uv sync

CMD [ "uv", "run", "python", "./bot.py" ]
