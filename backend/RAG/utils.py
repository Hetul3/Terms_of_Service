import os
from app.config import Config
from groq import Groq
import re
from collections import defaultdict
import chromadb
from chromadb.config import Settings
from chromadb import Client

groq_key = Config.GROQ_KEY
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../terms_vector_store')
collection_name = Config.COLLECTION_NAME

chroma_client = chromadb.PersistentClient(path=db_path)
collection = chroma_client.get_collection(name=collection_name)

# we will be using larger models for the generation and smaller models/specialized models for reasoning
generatorModels = ['llama-3.1-70b-versatile', 'llama3-70b-8192', 'llama3-groq-70b-8192-tool-use-preview']
reasoningModels = ['llama-3.1-8b-instant', 'llama3-8b-8192', 'mixtral-8x7b-32768', 'gemma2-9b-it']

def query_llm(prompt, max_tokens=100, temperature=0.3, model='llama-3.1-70b-versatile'):
    client = Groq(api_key=groq_key)
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return chat_completion.choices[0].message.content

def chunk_text(text, min_chunk_length=150, max_chunk_length=450):
    chunks = []
    current_chunk = ""
    words = re.split(r'(\s+)', text)
    
    for word in words:
        if len(current_chunk) + len(word) > max_chunk_length:
            chunks.append(current_chunk)
            current_chunk = ""
        else:
            current_chunk += word
        
        if len(current_chunk) >= min_chunk_length and re.search(r'[.!?]\s*$', current_chunk):
            chunks.append(current_chunk.strip())
            current_chunk = ""
    
    if current_chunk:
        chunks.append(current_chunk.strip())
        
    return chunks

def retrieve_from_vstore(text, including_data, n_results=3, collection=collection_name):
    client_collection = chroma_client.get_collection(name=collection)
    
    results = client_collection.query(
        query_texts=[text],
        n_results=n_results,
        include=including_data
    )
    return results