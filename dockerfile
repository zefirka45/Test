# Используем образ с предустановленным uv и Python 3.11
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY pyproject.toml uv.lock* ./

# Устанавливаем зависимости через uv
RUN uv sync --frozen --no-cache

# Копируем исходный код проекта
COPY . .

# Открываем порт для FastAPI
EXPOSE 8000

# Команда запуска сервера
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]