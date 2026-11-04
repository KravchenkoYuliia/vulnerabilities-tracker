FROM python:3.12-slim

RUN pip install --no-cache-dir requests psycopg2-binary python-dotenv
COPY seed_cve.py /seed_cve.py

CMD ["python3", "/seed_cve.py"]