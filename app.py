from flask import Flask, jsonify, request
from datetime import datetime
import logging
import os

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lista para almacenar comentarios
comments = []

@app.route('/')
def home():
    logger.info("Home endpoint accessed")
    return jsonify({
        "message": "Flask Comments API", 
        "version": "1.0.0",
        "endpoints": {
            "GET /comments": "Obtener todos los comentarios",
            "POST /comments": "Crear un nuevo comentario",
            "DELETE /comments/<id>": "Eliminar comentario",
            "GET /health": "Health check"
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

@app.route('/comments', methods=['GET'])
def get_comments():
    logger.info(f"Retrieved {len(comments)} comments")
    return jsonify({"comments": comments, "total": len(comments)})

@app.route('/comments', methods=['POST'])
def add_comment():
    data = request.get_json()
    if not data or 'content' not in data:
        logger.warning("Comment creation failed: missing content")
        return jsonify({"error": "Content is required"}), 400
    
    comment = {
        "id": len(comments) + 1,
        "content": data['content'],
        "author": data.get('author', 'Anonymous'),
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
