import sys
import os
import json
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from RAG.RAG_Models.dynamic_corrective_rag import CorrectiveRAG
from RAG.RAG_Models.rag import BaseRAG
from RAG.utils import retrieve_from_vstore, query_llm, chunk_text
from sklearn.metrics import precision_recall_fscore_support

def run_corrective_rag(input_data):
    model = CorrectiveRAG(generator_models=['llama-3.1-70b-versatile', 'llama3-70b-8192', 'llama3-groq-70b-8192-tool-use-preview'], reasoning_models=['llama-3.1-8b-instant', 'llama3-8b-8192', 'mixtral-8x7b-32768', 'gemma2-9b-it'])
    chunks = model.process_text(input_data)
    result_map = model.process_result_object(chunks)
    explanations = model.generate_explanations(result_map)
    classifications = {chunk: explanation['classification'] for chunk, explanation in explanations.items()}
    print("CRAG: ", classifications)
    return classifications
    
def run_rag(input_data):
    model = BaseRAG(generator_models=['llama-3.1-70b-versatile', 'llama3-70b-8192', 'llama3-groq-70b-8192-tool-use-preview'])
    explanations = model.process_text(input_data)
    classifications = {chunk: explanation['classification'] for chunk, explanation in explanations.items()}
    print("RAG: ", classifications)
    return classifications

def calculate_f1_score(true_labels, predicted_labels):
    precision, recall, f1, _ = precision_recall_fscore_support(
        true_labels, predicted_labels, average='weighted', zero_division=0
    )
    return precision, recall, f1

def benchmark_models(input_data, true_labels):
    corrective_classifications = run_corrective_rag(input_data)
    corrective_labels = list(corrective_classifications.values())
    
    rag_classifications = run_rag(input_data)
    rag_labels = list(rag_classifications.values())
    
    precision_corrective, recall_corrective, f1_corrective = calculate_f1_score(true_labels, corrective_labels)
    
    precision_rag, recall_rag, f1_rag = calculate_f1_score(true_labels, rag_labels)
    
    print("True labels:", true_labels)
    print("Corrective RAG predicted labels:", corrective_labels)
    print("Base RAG predicted labels:", rag_labels)
    
    print('Corrective RAG: ')
    print(f'Precision: {precision_corrective}, Recall: {recall_corrective}, F1: {f1_corrective}')
    
    print('RAG: ')
    print(f'Precision: {precision_rag}, Recall: {recall_rag}, F1: {f1_rag}')
    return f1_corrective, f1_rag
    
if __name__ == '__main__':
    test_cases = [
        ("We may collect information about your location and device usage to enhance your experience.", 'First Party Collection/Use'),
        ("Your data will be retained for as long as necessary to provide you with our services.", 'Data Retention'),
        ("If you have any questions about our privacy practices, you can contact us at privacy@example.com.", 'Privacy contact information'),
        ("Our service is not intended for use by children under the age of 13.", 'International and Specific Audiences'),
        ("We have implemented industry-standard security measures to protect your personal information.", 'Data Security'),
        ("Users can request access to, edit, or delete their personal information through their account settings.", '"User Access, Edit and Deletion"'),
        ("By using our service, you agree to the terms and conditions outlined in this agreement.", 'Introductory/Generic'),
        ("You have the option to opt-out of certain data collection practices at any time.", 'User Choice/Control'),
        ("We may share your information with trusted partners to provide and improve our services.", 'Third Party Sharing/Collection'),
    ]
    input_data_list = [input_data for input_data, _ in test_cases]
    true_labels_list = [true_label for _, true_label in test_cases]
    
    f1_corrective_scores = []
    f1_rag_scores = []
    
    for input_data, true_label in zip(input_data_list, true_labels_list):
        print(f"Testing with input: '{input_data}'")
        f1_corrective, f1_rag = benchmark_models(input_data, [true_label])
        f1_corrective_scores.append(f1_corrective)
        f1_rag_scores.append(f1_rag)
        print()
        
        # Wait for 1 minute (60 seconds) between each test case
        print("Waiting for 1 minute before the next test case...")
        time.sleep(60)
    
    # Calculate overall F1 score using macro averaging
    overall_f1_corrective = sum(f1_corrective_scores) / len(f1_corrective_scores)
    overall_f1_rag = sum(f1_rag_scores) / len(f1_rag_scores)

    print(f"Overall Corrective RAG F1 Score: {overall_f1_corrective}")
    print(f"Overall RAG F1 Score: {overall_f1_rag}")