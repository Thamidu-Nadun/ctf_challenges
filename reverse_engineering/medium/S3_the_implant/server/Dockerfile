# =====================================================================
#  S3 register server image (Flask)
# =====================================================================
FROM python:3.11-slim
RUN useradd -m -u 10003 s3svc
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
USER s3svc
EXPOSE 8080

CMD ["python", "/app/app.py"]
