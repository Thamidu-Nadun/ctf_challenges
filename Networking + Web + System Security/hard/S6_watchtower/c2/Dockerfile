#  C2 service image  (Flask)

FROM python:3.11-slim

# non-root user (privilege restriction — assignment §8)
RUN useradd -m -u 10001 c2svc

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .

USER c2svc
EXPOSE 8080

CMD ["python", "app.py"]
