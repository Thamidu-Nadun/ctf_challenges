
#  WATCHTOWER service image  (Flask + seed data)

FROM python:3.11-slim

RUN useradd -m -u 10002 wtsvc

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
COPY seed/ ./seed/

USER wtsvc
EXPOSE 9000
CMD ["python", "app.py"]
