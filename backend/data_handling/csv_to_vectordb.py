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
    
    
def create_vstore_with_size(size, name, data_path):
    chroma_client = chromadb.PersistentClient(path=db_path)
    collection = chroma_client.get_or_create_collection(name=name, metadata={"hnsw:space": "cosine"})
    print(f"size of the collection: {collection.count()}")
    
    existing_docs = collection.get(ids=[], limit=1)['documents']
    if len(existing_docs) > 0:
        print(f"Collection {name} already exists and is non-empty. No new data is added")
        print(f"Existing document: {existing_docs}")
        return False
    
    print(f"Collection {name} does not exist or is empty. Adding data")
    
    text_to_classifications = defaultdict(set)
    
    try:
        with open(data_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            documents = []
            ids = []
            metadatas = []

            for row in reader:
                text = row['text']
                classification = row['classification']
                text_to_classifications[text].add(classification)
                print(f"Read row: {text} -> {classification}")
            
            for text, classifications in list(text_to_classifications.items())[:size]:
                documents.append(text)
                ids.append(f"doc_{hash(text)}")
                metadatas.append({'classifications': json.dumps(list(classifications))})
                print(f"Adding document to collection: {text} with classifications: {classifications}")

            collection.add(
                documents=documents,
                ids=ids,
                metadatas=metadatas
            )
            print(f"Successfully added {len(documents)} documents to the collection.")

    except Exception as e:
        print(f"Error reading or adding data: {e}")
        return False

    return True
