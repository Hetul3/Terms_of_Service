import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
from llm import chunk_text, retrieve_from_vstore, query_llm
from .prompts import SYSTEM_PROMPT_GENERATION, SYSTEM_PROMPT_SPECIFICITY, SYSTEM_PROMPT_SIMILIARITY

class CorrectiveRAG:
    def __init__(self, generator_models, reasoning_models, max_tokens=100, temperature=0.2):
        self.generator_models = generator_models
        self.reasoning_models = reasoning_models
        self.max_tokens = max_tokens
        self.temperature = temperature
        
        
    def classify_prompt_text(self, prompt_text):
        classify_prompt = SYSTEM_PROMPT_SPECIFICITY.format(
            prompt_text=prompt_text,
        )
        response = query_llm(classify_prompt, max_tokens=15, temperature=0.0, model=self.reasoning_models[1])
        print("Raw LLM Response:", response)
        
        try:
            response_json = json.loads(response.strip())
            specificity_score = response_json.get("specificity", 0)
            threshold_score = 0.53 * (1 + (specificity_score / 10)) # Dynamic threshold based on empirical testing
            return threshold_score

        except json.JSONDecodeError:
            print("Error: Failed to decode JSON from LLM response.")
            return 0  

        except KeyError:
            print("Error: 'specificity' key not found in JSON response.")
            return 0  
        
    def determine_text_classification(self, cosine_similiarity, retrieved_text, prompt_text, threshold_score):
        find_similarity_llm = SYSTEM_PROMPT_SIMILIARITY.format(
            retrieved_text=retrieved_text,
            prompt_text=prompt_text
        )
        response = query_llm(find_similarity_llm, max_tokens=10, temperature=0.0, model=self.reasoning_models[2])
        try:
            response_json = json.loads(response)
            llm_similiarity = response_json.get("similarity", 0)
        except json.JSONDecodeError:
            llm_similiarity = 0
        
        similairity_score = (llm_similiarity + abs(cosine_similiarity)) / 2
        if(similairity_score >= threshold_score):
            return 'related'
        elif(similairity_score <= threshold_score and similairity_score > 0.2):
            return 'semi-related'
        else:
            return 'unrelated'
        
        
    def classify_retrieved_text(self, chunk, retrieved_data, classifications, cosine_similiarity):
        threshold_score = self.classify_prompt_text(chunk)
        classification = self.determine_text_classification(cosine_similiarity, retrieved_data, chunk, threshold_score)
        return classification
    
    def process_text(self, text):
        chunks = chunk_text(text)
        all_results = []
        
        for chunk in chunks:
            retrieval_results = retrieve_from_vstore(chunk, ['metadatas', 'documents', 'distances'])
            
            for doc, meta, dist in zip(retrieval_results['documents'],
                                       retrieval_results['metadatas'],
                                       retrieval_results['distances']):
                retrieved_classifications = meta.get('classifications', '[]')
                classification = self.classify_retrieved_text(chunk, doc, retrieved_classifications, dist)
                all_results.append({
                    'chunk': chunk,
                    'document': doc,
                    'relation': classification,
                    'classification': retrieved_classifications,
                    'refinement': None,
                    'distance': dist,
                })
                
            return all_results
        
    
    def knowledge_refinement(self, chunk, semi_related_docs):
        return "Refined knowledge"
        
    def knowledge_search(self, chunk):
        return "Searched knowledge"

    def generate_explanation(self, results):
        explanations = []
        chunks_grouped = {}
        
        for result in results:
            chunk = result['chunk']
            if chunk not in chunks_grouped:
                chunks_grouped[chunk] = {'related': [], 'semi-related': [], 'unrelated': [], 'unclassified': []} 
                
            chunks_grouped[chunk][result['relation']].append({
                'document': result['document'],
                'classification': resukt['classification'],
                'relation': result['relation'],
            })
            
        for chunk, docs_group in chunks_grouped.items():
            if doc_group['related']:
                related_docs = docs_group['related']
                prompt = SYSTEM_PROMPT_GENERATION.format(
                    chunk=chunk,
                    related_docs=related_docs
                )
                explanation = query_llm(prompt, max_tokens=25, temperature=self.temperature, model=self.generator_models[0])
                try:
                    response_json = json.loads(explanation)
                    explanation = response_json.get("explanation", "Introductory/Generic")
                except json.JSONDecodeError:
                    explanation = "Introductory/Generic"
                    
            elif docs_group['semi-related']:
                explanation = self.knowledge_refinement(chunk, docs_group['semi-related'])
            
            elif all(not docs for relation, docs in docs_group.items() if relation != 'unrelated' and relation != 'unclassified'):
                explanation = self.knowledge_search(chunk)
            
            else:
                continue
            
            explanations.append({
                'chunk': chunk,
                'explanation': explanation.strip(),
            })
        
        return explanations
    
    def testing():
        return "testing works"