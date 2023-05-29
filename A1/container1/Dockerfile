FROM python

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .

EXPOSE 6000

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "-p", "6000"]
