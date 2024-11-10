FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# ENV BOOTSTRAP_SERVER=<adres_bootstrap_serwera>
# ENV KAFKA_CONFLUENCE_API_KEY=<api_key>
# ENV KAFKA_CONFLUENCE_API_SECRET=<api_secret>

CMD ["python", "main.py"]
