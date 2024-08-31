import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
from utils import chunk_text, retrieve_from_vstore, query_llm
from .prompts import SYSTEM_PROMPT_GENERATION, SYSTEM_PROMPT_SPECIFICITY, SYSTEM_PROMPT_SIMILIARITY, SYSTEM_PROMPT_REPHRASE

class CorrectiveRAG:
    def __init__(self, generator_models, reasoning_models, max_tokens=100, temperature=0.3):
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
        response = query_llm(find_similarity_llm, max_tokens=15, temperature=0.0, model=self.reasoning_models[2])
        print("Raw LLM Response:", response)
        try:
            response_json = json.loads(response)
            llm_similiarity = response_json.get("similarity", 0)
        except json.JSONDecodeError:
            llm_similiarity = 0
        
        similairity_score = (llm_similiarity + abs(cosine_similiarity)) / 2
        if(similairity_score >= threshold_score):
            return 'related', similairity_score
        elif(similairity_score <= threshold_score and similairity_score > 0.2):
            return 'semi-related', similairity_score
        else:
            return 'unrelated', similairity_score
        
    
    def process_text(self, text):
        chunks = chunk_text(text)
        all_results = []
        threshold_score = self.classify_prompt_text(text)
        
        for chunk in chunks:
            retrieval_results = retrieve_from_vstore(chunk, ['metadatas', 'documents', 'distances'])
            
            for doc, meta, dist in zip(retrieval_results['documents'][0],
                                       retrieval_results['metadatas'][0],
                                       retrieval_results['distances'][0]):
                classifications_string = meta.get('classifications', '[]')
                retrieved_classifications = json.loads(classifications_string)
                classification, similarity_score = self.determine_text_classification(dist, doc, chunk, threshold_score)
                all_results.append({
                    'chunk': chunk,
                    'document': doc,
                    'relation': classification,
                    'classification': retrieved_classifications,
                    'refinement': None,
                    'distance': similarity_score,
                })
                
        return all_results
        
    def process_result_object(self, all_results):
        result_map = {}
        
        for result in all_results:
            chunk = result['chunk']
            
            if chunk not in result_map:
                result_map[chunk] = []
            
            result_map[chunk].append({
                'document': result['document'],
                'relation': result['relation'],
                'classification': result['classification'],
                'refinement': result['refinement'],
                'distance': result['distance'],
            })
        
        return result_map
        
    def knowledge_refinement(self, chunk):
        prompt = SYSTEM_PROMPT_REPHRASE.format(
            chunk=chunk
        )
        response = query_llm(prompt, max_tokens=75, temperature=self.temperature, model=self.generator_models[1])
        print("Raw LLM Response:", response)
        try:
            response_json = json.loads(response.strip())
            rephrased_chunk = response_json.get("rephrased_chunk", chunk)
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON from LLM response. Fallback to default chunk.")
            rephrased_chunk = chunk
        
        print("Rephrased chunk: ", rephrased_chunk)

        retrieval_results = retrieve_from_vstore(rephrased_chunk, ['documents', 'metadatas'], n_results=2)
        retrieval_results_arr = []
        for doc, meta in zip(retrieval_results['documents'][0], retrieval_results['metadatas'][0]):
            classifications_string = meta.get('classifications', '[]')
            retrieved_classifications = json.loads(classifications_string)
            retrieval_results_arr.append({
                'document': doc,
                'classification': retrieved_classifications,
            })
        
        retrieval_text = str(retrieval_results_arr)
        print("Retrieval text: ", retrieval_text)
        prompt = SYSTEM_PROMPT_GENERATION.format(
            chunk=rephrased_chunk,
            related_docs=retrieval_text
        )
        print("System prompt (ambigious): ", prompt)
        response = query_llm(prompt, max_tokens=75, temperature=self.temperature, model=self.generator_models[0])
        print("Raw LLM Response Generation:", response)
        try:
            response_json = json.loads(response.strip())
            explanation = response_json.get("explanation", "Introductory/Generic")
            classification = response_json.get("classification", "Introductory/Generic")
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON from LLM response. Fallback to default explanation.")
            explanation = "Introductory/Generic"
            classification = "Introductory/Generic"
        
        return explanation, classification
        
    def knowledge_search(self, chunk):
        # TODO: Implement web search/scraping for a legal knowledge base
        return "???", "???"
    
    
    def generate_explanations(self, result_map):
        explanations = {}
        for chunk, results in result_map.items():
            if chunk not in explanations:
                explanations[chunk] = {}
            
            related_docs = []
            semi_related_docs = []
            unrelated_docs = []
            for result in results:
                if result['relation'] == 'related':
                    related_docs.append({
                        'document': result['document'],
                        'classification': result['classification'],
                    })
                elif result['relation'] == 'semi-related':
                    semi_related_docs.append({
                        'document': result['document'],
                        'classification': result['classification'],
                    })
                else:
                    unrelated_docs.append({
                        'document': result['document'],
                        'classification': result['classification'],
                    })
                    
            explanation="Introductory/Generic"
            classification="Introductory/Generic"
                
            if related_docs:
                related_docs_str = json.dumps(related_docs)
                prompt = SYSTEM_PROMPT_GENERATION.format(
                    chunk=chunk,
                    related_docs=related_docs_str
                )
                print("System prompt: ", prompt)
                response = query_llm(prompt, max_tokens=75, temperature=self.temperature, model=self.generator_models[0])
                try:
                    response_json = json.loads(response.strip())
                    explanation = response_json.get("explanation", "Introductory/Generic")
                    classification = response_json.get("classification", "Introductory/Generic")
                except json.JSONDecodeError:
                    print("Error: Failed to decode JSON from LLM response. Fallback to default explanation.")
                    explanation = "Introductory/Generic"
                    classification = "Introductory/Generic"
            
            elif semi_related_docs:
                explanation, classification = self.knowledge_refinement(chunk)    
            else:
                explanation, classification = self.knowledge_search(chunk)
                
            explanations[chunk] = {
                'explanation': explanation.strip(),
                'classification': classification.strip()
            }
            
        return explanations           