from flask import jsonify, current_app, Response, json, request
import requests
from . import vector_store_bp
from data_handling.csv_to_vectordb import *

@vector_store_bp.route('/initialize_vstore', methods=['GET'])
def create_vstore_route():
    try:
        message = create_vstore()
        status_code = 200 if "successfully" in message else 500
        response = Response(json.dumps({'message': message}), status=status_code, mimetype='application/json')
        return response
    except Exception as e:
        current_app.logger.error(f"Error creating vector store: {e}")
        response = Response(json.dumps({'error': "Unexcepted error creating vector store"}), status=500, mimetype='application/json')
        return response