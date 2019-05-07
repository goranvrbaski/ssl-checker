FROM python:3.7-alpine

WORKDIR /app
COPY app.py .

ENTRYPOINT ["python", "app.py"]