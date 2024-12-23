FROM python:3.9-slim

WORKDIR /app

COPY backend/ .

RUN pip install -r requirements.txt

CMD ["python", "app.py"]