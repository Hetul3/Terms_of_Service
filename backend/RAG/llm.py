from utils import chunk_text, retrieve_from_vstore, query_llm, generatorModels, reasoningModels
from RAG_Models.dynamic_corrective_rag import CorrectiveRAG

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

def handle_text_contract(text):
    corrective_rag = CorrectiveRAG(generatorModels, reasoningModels)
    chunks = corrective_rag.process_text(text)
    result_map = corrective_rag.process_result_object(chunks)
    explanations = corrective_rag.generate_explanations(result_map)
    return explanations

if __name__ == "__main__":
    print("test")
    results = retrieve_from_vstore("contract law", ['metadatas', 'documents', 'distances'])
    print(results)