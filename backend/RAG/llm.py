import os
from app.config import Config
from groq import Groq
import re
from collections import defaultdict
import chromadb
from chromadb.config import Settings
from chromadb import Client
from RAG_Models.dynamic_corrective_rag import CorrectiveRAG

groq_key = Config.GROQ_KEY
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../terms_vector_store')
collection_name = Config.COLLECTION_NAME
# collection_name = "terms_and_conditions_classification_collection"

chroma_client = chromadb.PersistentClient(path=db_path)
# print(chroma_client.list_collections())
collection = chroma_client.get_collection(name=collection_name)

# we will be using larger models for the generation and smaller models/specialized models for reasoning
generatorModels = ['llama-3.1-70b-versatile', 'llama3-70b-8192', 'llama3-groq-70b-8192-tool-use-preview']
reasoningModels = ['llama-3.1-8b-instant', 'llama3-8b-8192', 'mixtral-8x7b-32768', 'gemma2-9b-it']

# general functiont to query for an llm response for testing
def query_llm(prompt, max_tokens=100, temperature=0.3, model=generatorModels[0]):
    client = Groq(
        api_key=groq_key,
    )
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ], 
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    print(chat_completion.choices[0].message)
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
            current_chunk+=word
        
        if len(current_chunk) >= min_chunk_length and re.search(r'[.!?]\s*$', current_chunk):
            chunks.append(current_chunk.strip())
            current_chunk = ""
    
    if current_chunk:
        chunks.append(current_chunk.strip())
        
    return chunks

def retrieve_from_vstore(text, including_data, n_results=3):
    results = collection.query(
        query_texts=[text],
        n_results=n_results,
        include=including_data
    )
    return results

def pair_chunks_with_results(chunks, n_results=3):
    result_dict = {}
    
    for chunk in chunks:
        results = retrieve_from_vstore(chunk, ['metadatas', 'documents', 'distances'], n_results)
        
        documents = []
        metadatas = []
        distances = []
        
        for doc_list, meta_list, dist_list in zip(results['documents'], results['metadatas'], results['distances']):
            documents.extend(doc_list)
            metadatas.extend(meta_list)
            distances.extend(dist_list)
            
        result_dict[chunk] = {
            "documents": documents,
            "metadatas": metadatas,
            "distances": distances
        }
    return result_dict
        
        
if __name__ == "__main__":
    print("test")
    results = retrieve_from_vstore("contract law", ['metadatas', 'documents', 'distances'])
    print(results)
    

def handle_text_contract(text):
    chunks = CorrectiveRAG.process_text(text)
    result_map = CorrectiveRAG.process_result_object(chunks)
    explanations = CorrectiveRAG.generate_explanations(result_map)