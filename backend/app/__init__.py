from flask import Flask
import os
from .config import Config
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    app.config.from_object(Config)
    
    from .routes import vector_store_bp, rag_bp, feedback_bp
    app.register_blueprint(vector_store_bp, url_prefix='/vector_store')
    app.register_blueprint(rag_bp, url_prefix='/rag')
    app.register_blueprint(feedback_bp, url_prefix='/feedback')
    
    return app