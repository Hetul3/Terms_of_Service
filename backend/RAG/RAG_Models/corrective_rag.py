import os
from '../llm' import chunk_text, retrieve_from_vstore, query_llm
from prompts import SYSTEM_PROMPT_EVALUATION, SYSTEM_PROMPT_REFINEMENT, SYSTEM_PROMPT_GENERATION

class CorrectiveRAG:
    def __init__(self, generator_models, reasoning_models, chroma_collection, max_tokens=100, temperature=0.2):
        self.generator_models = generator_models
        self.reasoning_models = reasoning_models
        self.chroma_collection = chroma_collection
        self.max_tokens = max_tokens
        self.temperature = temperature
        
    def classify_retrieved_text(self, chunk, retrieved_data, classifications):
        classification_prompt = SYSTEM_PROMPT_EVALUATION.format(
            chunk=chunk,
            retrieved_data=retrieved_data,
            classifications=classifications
        )
        
        response = query_llm(classification_prompt, max_tokens=10, temperature=0.1, model=self.reasoning_models[0])
        
        classification = response.strip().lower()
        
        max_attempts = 2
        
        while classification not in ['related', 'semi-related', 'unrelated']:
            if(max_attempts == 0):
                return None
            print(f"Unexpected classification: {response}. Re-evaluating")
            response = query_llm(classification_prompt, max_tokens=10, temperature=0.1, model=self.reasoning_models[0])
            classification = response.strip().lower()
            max_attempts -= 1
            
        if classification not in ['related', 'semi-related', 'unrelated']:
            return "unclassified"
        
        return classification
    
    def process_text(self, text):
        chunks = chunk_text(text)
        all_results = []

        for chunk in chunks:
            retrieval_results = retrieve_from_vstore(chunk, ['metadatas', 'documents', 'distances'])
            
            for doc, meta, dist in zip(retrieval_results['documents'], 
                                    retrieval_results['metadatas'], 
                                    retrieval_results['distances']):
                
                classifications = meta.get('classifications', '[]')
                classification = self.classify_retrieved_text(chunk, doc, classifications)
                
                all_results.append({
                    'chunk': chunk,
                    'document': doc,
                    'classification': classification,
                    'refinement': None,
                    'distance': dist,
                    'metadata': meta,
                })

        return all_results

    def generate_explanation(self, results):
        explanations = []
        
        chunks_grouped = {}
        
        for result in results:
            if result['classification'] in ['unrelated', 'unclassified']:
                continue
            
            chunk = result['chunk']
            if chunk not in chunks_grouped:
                chunks_grouped[chunk] = []
                
            chunks_grouped[chunk].append({
                'document': result['document'],
                'classification': result['classification'],
                'metadata': result['metadata'],
                'distance': result['distance']
            })
            
        for chun, related_docs in chunks_grouped.items():
            doc_info = []
            
            for doc_info_item in related_docs:
                doc_info.append({
                    'document': doc_info_item['document'],
                    'classification': doc_info_item['metadata']['classification'],
                    'relation_score': doc_info_item['classification']
                })
            
            prompt = SYSTEM_PROMPT_REFINEMENT.format(
                chunk=chunk,
                related_docs=doc_info
            )
            
            explanation = query_llm(prompt, max_tokens=25, temperature=self.temperature, model=self.generator_models[0])
            explanations.append({
                'chunk': chunk,
                'explanation': explanation
            })
    
        return explanations