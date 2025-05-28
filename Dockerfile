FROM python:3.11-slim

WORKDIR /app
COPY ./lab5 /app


COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "lab5.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
