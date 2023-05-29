FROM python

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .


EXPOSE 7000

CMD ["python", "-m", "flask", "run", "--host=localhost", "-p", "7000"]
