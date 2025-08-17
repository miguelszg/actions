@"
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "app:app"]
"@ | Out-File -FilePath "Dockerfile" -Encoding UTF8

git add Dockerfile
git commit -m "feat: add Dockerfile for containerization"
git push origin main