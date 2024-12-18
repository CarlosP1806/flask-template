FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 5000

CMD ["sh", "-c", "if [ \"$ENV\" = 'production' ]; then gunicorn --bind 0.0.0.0:5000 \"api:create_app()\"; else flask --app api run --host=0.0.0.0 --port=5000; fi"]
