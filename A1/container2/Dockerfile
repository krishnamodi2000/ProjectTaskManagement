FROM python

WORKDIR /usr

COPY ./ ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7000

CMD ["python", "container2.py"]
