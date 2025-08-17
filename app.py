# Actualizar app.py
@"
from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# Lista para almacenar comentarios (simulando base de datos)
comments = []

@app.route('/')
def home():
    return jsonify({
        "message": "Flask Comments API", 
        "version": "1.0.0",
        "endpoints": {
            "GET /comments": "Obtener todos los comentarios",
            "POST /comments": "Crear un nuevo comentario",
            "GET /health": "Health check"
        }
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy", 
        "service": "flask-comments-api",
        "timestamp": datetime.now().isoformat(),
        "total_comments": len(comments)
    })

@app.route('/comments', methods=['GET'])
def get_comments():
    return jsonify({"comments": comments, "total": len(comments)})

@app.route('/comments', methods=['POST'])
def add_comment():
    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({"error": "Content is required"}), 400
    
    comment = {
        "id": len(comments) + 1,
        "content": data['content'],
        "author": data.get('author', 'Anonymous'),
        "timestamp": datetime.now().isoformat()
    }
    comments.append(comment)
    return jsonify(comment), 201


@app.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    global comments
    comments = [c for c in comments if c['id'] != comment_id]
    return jsonify({"message": f"Comment {comment_id} deleted"}), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
"@ | Out-File -FilePath "app.py" -Encoding UTF8

git add app.py
git commit -m "feat: add comments API endpoints (GET, POST)"
git push origin main

