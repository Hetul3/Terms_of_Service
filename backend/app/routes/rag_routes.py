from flask import jsonify, current_app, Response, json, request
from werkzeug.utils import secure_filename
import requests
from . import rag_bp
from RAG.llm import *

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
    
# process the contract string and return the results
@rag_bp.route('/process_text_contract', methods=['POST'])
def process_text_contract():
    try:
        data = request.get_json()
        text = data.get('text')
        processed_response = handle_text_contract(text)
        # handle how to process the text contract and send back response in reasonable manner
        response = Response(json.dunps({'response': processed_response}), status=200, mimetype='application/json')
        return response
    except Exception as e:
        current_app.logger.error(f"Error processing text contract: {e}")
        response = Response(json.dumps({'error': "Unexpected error processing text contract"}), status=500, mimetype='application/json')
        return response
    
@rag_bp.route('/process_image_contract', methods=['POST'])
def process_image_contract():
    try:
        text = None
        
        if 'file' not in request.files:
            response = Response(json.dumps({'error': "No file part in the request"}), status=400, mimetype='application/json')
            return response

        file = request.files['file']

        if file.filename == '':
            response = Response(json.dumps({'error': "No selected file"}), status=400, mimetype='application/json')
            return response

        if file:
            filename = secure_filename(file.filename)
            text = extract_image_text(file)

        if text is None:
            response = Response(json.dumps({'error': "No text extracted from file"}), status=400, mimetype='application/json')
            return response

        processed_response = handle_text_contract(text)
        
        # handle how to process the text contract and send back response in reasonable manner
        response = Response(json.dumps({'response': processed_response}), status=200, mimetype='application/json')
        return response
    except Exception as e:
        current_app.logger.error(f"Error processing text contract: {e}")
        response = Response(json.dumps({'error': "Unexpected error processing text contract"}), status=500, mimetype='application/json')
        return response
        
@rag_bp.route('/process_url_contract', methods=['POST'])
def process_url_contract():
    try:
        data = request.get_json()
        url = data.get('url')
        extracted_text = None
        try:
            extracted_text = scrape_url(url)
            if extracted_text is None:
                response = Response(json.dumps({'error': "No text extracted from URL"}), status=400, mimetype='application/json')
                return response
        except Exception as e:
            response = Response(json.dumps({'error': "Error extracting text from URL"}), status=400, mimetype='application/json')
            return response
        
        processed_response = handle_text_contract(extracted_text)
        
        # handle how to process the text contract and send back response in reasonable manner
        response = Response(json.dumps({'response': processed_response}), status=200, mimetype='application/json')
        return response
    except Exception as e:
        current_app.logger.error(f"Error processing text contract: {e}")
        response = Response(json.dumps({'error': "Unexpected error processing text contract"}), status=500, mimetype='application/json')
        return response