# 使用官方的Python基礎映像
FROM python:3.11-slim

# 設置工作目錄
WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 複製pyproject.toml和poetry.lock到工作目錄
COPY pyproject.toml poetry.lock* /app/

# 安裝poetry
RUN pip install poetry

# 使用poetry安裝Python依賴
RUN poetry config virtualenvs.create false \
    && poetry install --only main \
    || poetry install --only main --no-root

# 複製應用程式源代碼到工作目錄
COPY . /app

# 設置環境變量
ENV PYTHONBUFFERED=1

EXPOSE 8080

CMD uwsgi -w app:app --http :$PORT
