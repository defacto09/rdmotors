# Вказуємо базовий образ
FROM python:3.11-slim

# Копіюємо файли в контейнер
COPY . /app
WORKDIR /app

# Встановлюємо залежності
RUN pip install -r requirements.txt

# Запускаємо додаток
CMD ["python", "main.py"]