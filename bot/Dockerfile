FROM python:3.10-alpine
RUN pip install --no-cache-dir poetry
COPY pyproject.toml poetry.lock  /app/
WORKDIR /app/bot
RUN poetry config virtualenvs.create false && poetry install -n --no-ansi --only main
COPY .env /app/.env
COPY secrets/ /app/secrets
COPY . /app/bot
CMD ["poetry", "run", "python3.10", "main.py" ]