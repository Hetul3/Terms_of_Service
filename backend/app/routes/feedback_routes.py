from flask import jsonify, current_app, Response, json, request
import requests
from . import feedback_bp
from ..services.crud_operations import *
from app.config import Config

@feedback_bp.route('/create', methods=['POST'])
def create_feedback_table():
    data = request.json
    result = create_record(Config.TABLE_NAME, data)
    return jsonify(result), 201
    
@feedback_bp.route('/read', methods=['GET'])
def read_feedback_table():
    filters = request.args.to_dict()
    result = read_records(Config.TABLE_NAME, filters)
    return jsonify(result), 200

@feedback_bp.route('/update', methods=['PUT'])
def update_feedback_table():
    filters = request.json.get('filters')
    updates = request.json.get('updates')
    result = update_record(Config.TABLE_NAME, filters, updates)
    return jsonify(result), 200

@feedback_bp.route('/delete', methods=['DELETE'])
def delete_example():
    filters = request.json
    result = delete_record(Config.TABLE_NAME, filters)
    return jsonify(result), 200