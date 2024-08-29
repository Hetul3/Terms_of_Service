import os
import csv
import json
from collections import defaultdict
import chromadb
from dotenv import load_dotenv
from chromadb.config import Settings
from chromadb import Client
from app.config import Config
from .preprocessing import combine_csv

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../terms_vector_store')
collection_name = Config.COLLECTION_NAME

def create_vstore():
    data_path = combine_csv()
    
    chroma_client = chromadb.PersistentClient(path=db_path)
    collection = chroma_client.get_or_create_collection(name=collection_name, metadata={"hnsw:space": "cosine"})
    
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
        return f"Vectordb successfully stored"
    else:
        return f"Failed to store vectordb"