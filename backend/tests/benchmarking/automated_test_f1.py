import sys
import os
import json
import re
import csv
from collections import defaultdict
import chromadb
from chromadb.config import Settings
from chromadb import Client
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from RAG.RAG_Models.dynamic_corrective_rag import CorrectiveRAG
from RAG.RAG_Models.rag import BaseRAG
from RAG.utils import retrieve_from_vstore, query_llm, chunk_text
from data_handling.csv_to_vectordb import create_vstore_with_size

csv_data_path = '../../Legal_Doc_Dataset/dataset.csv'
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../terms_vector_store')

chroma_client = chromadb.PersistentClient(path=db_path)
vstore_name = 'automated_vstore_190302'

def define_testing_dataset(vstore_size=500, testing_size=20):
    _ = create_vstore_with_size(size=vstore_size, name=vstore_name, data_path=csv_data_path)
    collection = chroma_client.get_collection(name=vstore_name)
    
    testing_dataset = []
    
    with open(csv_data_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        header = next(reader)
        
        for _ in range(vstore_size):
            next(reader, None)
            
        for _ in range(testing_size):
            try:
                row = next(reader)
                testing_dataset.append({
                    'text': row['text'],
                    'classification': row['classification']
                })    
            except StopIteration:
                break
    
    print(testing_dataset)
    return testing_dataset

def run_corrective_rag(testing_dataset):
    model = CorrectiveRAG(generator_models=['llama-3.1-70b-versatile', 'llama3-70b-8192', 'llama3-groq-70b-8192-tool-use-preview'], reasoning_models=['llama-3.1-8b-instant', 'llama3-8b-8192', 'mixtral-8x7b-32768', 'gemma2-9b-it'], collection_name=vstore_name)
    chunks = model.process_text(testing_dataset)
    result_map = model.process_result_object(chunks)
    explanations = model.generate_explanations(result_map)
    classifications = {chunk: explanation['classification'] for chunk, explanation in explanations.items()}
    print("CRAG: ", classifications)
    return classifications


def run_rag(testing_dataset):
    model = BaseRAG(generator_models=['llama-3.1-70b-versatile', 'llama3-70b-8192', 'llama3-groq-70b-8192-tool-use-preview'], collection_name=vstore_name)
    explanations = model.process_text(testing_dataset)
    classifications = {chunk: explanation['classification'] for chunk, explanation in explanations.items()}
    print("RAG: ", classifications)
    return classifications

if __name__ == '__main__':
    define_testing_dataset()    