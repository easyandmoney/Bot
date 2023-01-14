FROM python:3.10.7-slim
WORKDIR /app
RUN pip install --no-cache-dir poetry
COPY poetry.lock pyproject.toml /app/
COPY bot /app/bot
CMD ["python", "-m", "bot"]


