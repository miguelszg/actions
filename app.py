from flask import Flask, jsonify, request
from datetime import datetime
import logging
import os
import re

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lista para almacenar comentarios
comments = []

def validate_comment_input(data):
    """Validar entrada de comentarios con seguridad"""
    if not data:
        return False, "No data provided"
    
    content = data.get('content', '').strip()
    author = data.get('author', 'Anonymous').strip()
    
    # Validar contenido
    if not content:
        return False, "Content cannot be empty"
    if len(content) > 1000:
        return False, "Content too long (max 1000 characters)"
    if len(author) > 100:
        return False, "Author name too long (max 100 characters)"
    
    # Detectar contenido potencialmente malicioso
    dangerous_patterns = [
        r'<script.*?>.*?</script>',
        r'javascript:',
        r'data:text/html',
        r'vbscript:',
        r'onload=',
        r'onerror='
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return False, "Invalid content detected"
    
    return True, "Valid input"

@app.route('/')
def home():
    logger.info("Home endpoint accessed")
    return jsonify({
        "message": "Flask Comments API", 
        "version": "1.2.0",
        "endpoints": {
            "GET /comments": "Obtener todos los comentarios",
            "POST /comments": "Crear un nuevo comentario",
            "DELETE /comments/<id>": "Eliminar comentario",
            "GET /health": "Health check",
            "GET /stats": "Estadísticas de la API"
        }
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy", 
        "service": "flask-comments-api",
        "timestamp": datetime.now().isoformat(),
        "total_comments": len(comments),
        "environment": os.getenv('ENVIRONMENT', 'development')
    })

@app.route('/stats')
def stats():
    if not comments:
        return jsonify({
            "total_comments": 0,
            "last_comment": None,
            "authors": [],
            "comments_today": 0
        })
    
    # Contar autores únicos
    authors = list(set([c.get('author', 'Anonymous') for c in comments]))
    
    # Contar comentarios de hoy
    today = datetime.now().date()
    comments_today = sum(1 for c in comments 
                        if datetime.fromisoformat(c['timestamp']).date() == today)
    
    return jsonify({
        "total_comments": len(comments),
        "last_comment": comments[-1],
        "authors": authors,
        "unique_authors": len(authors),
        "comments_today": comments_today
    })

@app.route('/comments', methods=['GET'])
def get_comments():
    logger.info(f"Retrieved {len(comments)} comments")
    return jsonify({"comments": comments, "total": len(comments)})

@app.route('/comments', methods=['POST'])
def add_comment():
    data = request.get_json()
    
    # Validar entrada
    is_valid, message = validate_comment_input(data)
    if not is_valid:
        logger.warning(f"Comment validation failed: {message}")
        return jsonify({"error": message}), 400
    
    comment = {
        "id": len(comments) + 1,
        "content": data['content'].strip(),
        "author": data.get('author', 'Anonymous').strip()[:100],
        "timestamp": datetime.now().isoformat()
    }
    comments.append(comment)
    logger.info(f"New comment created with ID: {comment['id']}")
    return jsonify(comment), 201

@app.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    global comments
    initial_count = len(comments)
    comments = [c for c in comments if c['id'] != comment_id]
    
    if len(comments) < initial_count:
        logger.info(f"Comment {comment_id} deleted")
        return jsonify({"message": f"Comment {comment_id} deleted"}), 200
    else:
        logger.warning(f"Comment {comment_id} not found for deletion")
        return jsonify({"error": "Comment not found"}), 404

@app.errorhandler(404)
def not_found(error):
    logger.warning("404 error occurred")
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error("500 error occurred")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
