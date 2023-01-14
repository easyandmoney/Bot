FROM python:3.10.7-slim
ENV POETRY_VIRTUALENVS_CREATE=falseRUN poetry install --no-dev --no-root
WORKDIR /app
RUN pip install --no-cache-dir poetry
COPY poetry.lock pyproject.toml /app/
RUN poetry install --no-dev --no-root
COPY bot /app/bot
CMD ["python", "-m", "bot"]


