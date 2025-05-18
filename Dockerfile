# Базовий образ
FROM --platform=linux/amd64 python:3.9-slim

# Створити робочу директорію
WORKDIR /app

# Скопіювати залежності
COPY requirements.txt .

# Встановити залежності
RUN pip install --no-cache-dir -r requirements.txt

# Скопіювати весь проєкт у контейнер
COPY . .

# Вказати змінну середовища (можна перевизначити через -e DB_PATH=...)
ENV DB_PATH=/app/database/rdmotors.db

# Запуск бота
CMD ["python", "main.py"]