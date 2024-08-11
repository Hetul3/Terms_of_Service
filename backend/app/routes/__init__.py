from flask import Blueprint

vector_store_bp = Blueprint('vector_store', __name__)
rag_bp = Blueprint('rag', __name__)

from . import vector_store_routes, rag_routes