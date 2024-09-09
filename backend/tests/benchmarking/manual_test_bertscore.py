import sys
import os
import json
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from RAG.RAG_Models.dynamic_corrective_rag import CorrectiveRAG
from RAG.RAG_Models.rag import BaseRAG
from RAG.utils import retrieve_from_vstore, query_llm, chunk_text
from bert_score import score
from .manual_test_cases.testcases import TEST_CASES_BERTSCORE

def run_corrective_rag(input_data):
    model = CorrectiveRAG(generator_models=['llama-3.1-70b-versatile', 'llama3-70b-8192', 'llama3-groq-70b-8192-tool-use-preview'], reasoning_models=['llama-3.1-8b-instant', 'llama3-8b-8192', 'mixtral-8x7b-32768', 'gemma2-9b-it'])
    chunks = model.process_text(input_data)
    result_map = model.process_result_object(chunks)
    explanations = model.generate_explanations(result_map)
    output = {chunk: {'explanation': explanation['explanation'], 'classification': explanation['classification']}
              for chunk, explanation in explanations.items()}
    print("CRAG Output: ", output)
    return output

def run_rag(input_data):
    model = BaseRAG(generator_models=['llama-3.1-70b-versatile', 'llama3-70b-8192', 'llama3-groq-70b-8192-tool-use-preview'])
    explanations = model.process_text(input_data)
    output = {chunk: {'explanation': explanation['explanation'], 'classification': explanation['classification']}
              for chunk, explanation in explanations.items()}
    print("RAG Output: ", output)
    return output

def calculate_bertscore(references, candidates, model_type='microsoft/deberta-xlarge-mnli'):
    P, R, F1 = score(candidates, references, model_type=model_type, lang='en', verbose=True)
    return P.mean().item(), R.mean().item(), F1.mean().item()

def benchmark_models(test_cases):
    corrective_explanations = []
    rag_explanations = []
    true_explanations = []
    
    for input_data, true_explanation in test_cases:
        corrective_classifications = run_corrective_rag(input_data)
        rag_classifications = run_rag(input_data)
        
        corrective_explanations.extend([explanation['explanation'] for explanation in corrective_classifications.values()])
        rag_explanations.extend([explanation['explanation'] for explanation in rag_classifications.values()])
        true_explanations.extend([true_explanation] * len(corrective_classifications))
    
        print("True labels:", true_explanations)
        print("Corrective RAG predicted labels:", corrective_explanations)
        print("Base RAG predicted labels:", rag_explanations)
        
        time.sleep(60)
    
    P_corrective, R_corrective, F1_corrective = calculate_bertscore(true_explanations, corrective_explanations)
    P_rag, R_rag, F1_rag = calculate_bertscore(true_explanations, rag_explanations)
    
    print('Overall BERTScore for Corrective RAG: Precision = ', P_corrective, 'Recall = ', R_corrective, 'F1 = ', F1_corrective)
    print('Overall BERTScore for Base RAG: Precision = ', P_rag, 'Recall = ', R_rag, 'F1 = ', F1_rag)
    
    return F1_corrective, F1_rag

if __name__ == '__main__':
    F1_corrective, F1_rag = benchmark_models(TEST_CASES_BERTSCORE)
    print('F1 Score for Corrective RAG: ', F1_corrective)
    print('F1 Score for Base RAG: ', F1_rag)