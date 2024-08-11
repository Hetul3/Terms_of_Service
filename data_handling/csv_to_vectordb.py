import os
import requests
import csv
import json
from collections import defaultdict
import chromadb
from chromadb.config import Settings
from chromadb import Client

db_path = '../vector_store'
data_path = 'dataset.csv'

def create_vstore():
    chroma_client = chromadb.PersistentClient(path=db_path)
    collection = chroma_client.get_or_create_collection(name='terms_and_classification_collection')
    
    text_to_classifications = defaultdict(set)
    
    with open(data_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        documents = []
        ids = []
        metadatas = []

        for row in reader:
            text = row['text']
            classification = row['classification']
            text_to_classifications[text].add(classification)
            
        for text, classifications in text_to_classifications.items():
            documents.append(text)
            ids.append(f"doc_{hash(text)}")
            metadatas.append({'classifications': json.dumps(list(classifications))})
            
        collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )
    
    if os.path.exists(db_path) and os.path.isdir(db_path):
        print(f"Vectordb successfully stored in {db_path}")
    else:
        print(f"Failed to store vectordb in {db_path}")
    
    print(f"Size of the collection: {collection.count()} documents")  
        
create_vstore()