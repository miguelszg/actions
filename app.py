# Crear app.py básico
@"
from flask import Flask, jsonify, request

app = Flask(__name__)

# Lista para almacenar comentarios (simulando base de datos)
comments = []

@app.route('/')
def home():
    return jsonify({"message": "Flask Comments API", "version": "1.0.0"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "flask-comments-api"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
"@ | Out-File -FilePath "app.py" -Encoding UTF8

# Crear requirements.txt
@"
Flask==2.3.3
gunicorn==21.2.0
"@ | Out-File -FilePath "requirements.txt" -Encoding UTF8

git add .
git commit -m "feat: initial Flask app structure with health endpoint"
git push origin main