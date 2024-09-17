import sys
import os
import json
import re
import csv
import time
from collections import defaultdict
import chromadb
from chromadb.config import Settings
from chromadb import Client
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from RAG.RAG_Models.dynamic_corrective_rag import CorrectiveRAG
from RAG.RAG_Models.rag import BaseRAG
from RAG.utils import retrieve_from_vstore, query_llm, chunk_text
from data_handling.csv_to_vectordb import create_vstore_with_size
from sklearn.metrics import precision_recall_fscore_support

csv_data_path = '../../Legal_Doc_Dataset/dataset.csv'
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../terms_vector_store')

chroma_client = chromadb.PersistentClient(path=db_path)
vstore_name = 'automated_vstore_190302'

def define_testing_dataset(vstore_size=500, testing_size=20):
    _ = create_vstore_with_size(size=vstore_size, name=vstore_name, data_path=csv_data_path)
    collection = chroma_client.get_collection(name=vstore_name)
    
    testing_dataset = defaultdict(list)
    
    with open(csv_data_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        header = next(reader)
        
        for _ in range(vstore_size):
            next(reader, None)
            
        for _ in range(testing_size):
            try:
                row = next(reader)
                testing_dataset[row['text']].append(row['classification'])
            except StopIteration:
                break
    
    return dict(testing_dataset)

def run_corrective_rag(testing_dataset):
    model = CorrectiveRAG(generator_models=['llama-3.1-70b-versatile', 'llama3-70b-8192', 'llama3-groq-70b-8192-tool-use-preview'], reasoning_models=['llama-3.1-8b-instant', 'llama3-8b-8192', 'mixtral-8x7b-32768', 'gemma2-9b-it'], collection_name=vstore_name)
    chunks = model.process_text(testing_dataset)
    result_map = model.process_result_object(chunks)
    explanations = model.generate_explanations(result_map)
    classifications = {chunk: explanation['classification'] for chunk, explanation in explanations.items()}
    return classifications

def run_rag(testing_dataset):
    model = BaseRAG(generator_models=['llama-3.1-70b-versatile', 'llama3-70b-8192', 'llama3-groq-70b-8192-tool-use-preview'], collection_name=vstore_name)
    explanations = model.process_text(testing_dataset)
    classifications = {chunk: explanation['classification'] for chunk, explanation in explanations.items()}
    return classifications

def calculate_f1_score(true_labels, predicted_labels):
    new_true_labels = []
    new_predicted_labels = []

    for true, pred in zip(true_labels, predicted_labels):
        if pred in true:
            new_true_labels.append(pred)  
            new_predicted_labels.append(pred)  
        else:
            new_true_labels.append(true[0])  
            new_predicted_labels.append(pred)  

    precision, recall, f1, _ = precision_recall_fscore_support(
        new_true_labels, new_predicted_labels, average='weighted', zero_division=0
    )

    return precision, recall, f1

def calculate_score(true_labels, predicted_labels):
    correct_predictions = set(true_labels) & set(predicted_labels)
    score = len(correct_predictions) / len(predicted_labels) if predicted_labels else 0
    return score

def benchmark_models(input_text, true_labels):
    corrective_classifications = run_corrective_rag([input_text])
    rag_classifications = run_rag([input_text])
    
    corrective_labels = list(corrective_classifications.values())
    rag_labels = list(rag_classifications.values())
    
    corrective_score = calculate_score(true_labels, corrective_labels)
    rag_score = calculate_score(true_labels, rag_labels)
    
    print(f"Input text: '{input_text[:100]}...' (truncated)")
    print(f"True labels: {true_labels}")
    print(f"Corrective RAG predicted labels: {corrective_labels}")
    print(f"Base RAG predicted labels: {rag_labels}")
    print(f"Corrective RAG score: {corrective_score:.2f}")
    print(f"Base RAG score: {rag_score:.2f}")
    
    return corrective_score, rag_score

if __name__ == '__main__':
    testing_dataset = define_testing_dataset()
    
    corrective_successes = []
    rag_successes = []
    
    for input_text, true_labels in testing_dataset.items():
        corrective_success, rag_success = benchmark_models(input_text, true_labels)
        corrective_successes.append(corrective_success)
        rag_successes.append(rag_success)
        time.sleep(60)
    
    corrective_average = sum(corrective_scores) / len(corrective_scores)
    rag_average = sum(rag_scores) / len(rag_scores)
    
    print("\nOverall Results:")
    print(f"Corrective RAG Accuracy: {corrective_accuracy:.2f}")
    print(f"Base RAG Accuracy: {rag_accuracy:.2f}")