# Базовый образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем  файл с зависимостями
COPY requirements.txt .

# Устанавливаем  зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY src/ ./src/

# Команда запуска по умолчанию 
CMD ["python", "src/main.py"]
