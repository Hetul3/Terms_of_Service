import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
from utils import chunk_text, retrieve_from_vstore, query_llm
from app.config import Config
from .prompts import SYSTEM_DIRECT_GENERATION


class BaseRAG:
    def __init__(self, generator_models, max_tokens=100, temperature=0.3, collection_name=Config.COLLECTION_NAME):
        self.generator_models = generator_models
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.collection_name = collection_name
    
    def process_text(self, text):
        chunks = chunk_text(text)
        explanations = {}
        
        for chunk in chunks:
            if chunk not in explanations:
                explanations[chunk] = {}
                
            retrieval_results = retrieve_from_vstore(chunk, ['metadatas', 'documents'], n_results=1, collection=self.collection_name)
            
            doc = retrieval_results['documents'][0][0]
            classification_string = retrieval_results['metadatas'][0][0].get('classifications', '[]')
            prompt = SYSTEM_DIRECT_GENERATION.format(
                chunk=chunk,
                related_doc=doc,
                classifications=classification_string,
            )
            
            response = query_llm(prompt, max_tokens=self.max_tokens, temperature=self.temperature, model=self.generator_models[2])
            try:
                response_json = json.loads(response.strip())
                explanation = response_json.get("explanation", "Intrductory/Generic")
                classification = response_json.get("classification", "Introductory/Generic")
            except json.JSONDecodeError:
                print("Error: Failed to decode JSON from LLM response. Fallback to default explanation.")
                explanation = "Introductory/Generic"
                classification = "Introductory/Generic"
            
            explanations[chunk] = {
                'explanation': explanation,
                'classification': classification,
            }
            
        return explanations