from flask import jsonify, current_app, requests, Response, json
from . import rag_bp
from app.RAG.llm import *

# query the LLM directly and save the query and results in db
@rag_bp.route('/query_llm', methods=['POST'])
def query_llm_directly():
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        chat_response = query_llm(prompt)
        response = Response(json.dumps({'response': chat_response}), status=200, mimetype='application/json')
        return response
    except Exception as e:
        current_app.logger.error(f"Error querying LLM: {e}")
        response = Response(json.dumps({'error': "Unexpected error querying LLM"}), status=500, mimetype='application/json')
        return response