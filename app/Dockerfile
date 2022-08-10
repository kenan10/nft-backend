FROM python:3.10.6-slim-buster

COPY /app /usr/backend/app
WORKDIR /usr/backend
COPY requirements.txt .
COPY .env .
RUN pip3 install --no-cache-dir -r requirements.txt
WORKDIR /usr/backend/app/db
RUN alembic upgrade heads
WORKDIR /usr/backend
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
