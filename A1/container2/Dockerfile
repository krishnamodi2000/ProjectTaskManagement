FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .

EXPOSE 8081

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "-p", "8081"]
