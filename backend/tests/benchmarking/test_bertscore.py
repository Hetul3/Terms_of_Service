import sys
import os
import json
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from RAG.RAG_Models.dynamic_corrective_rag import CorrectiveRAG
from RAG.RAG_Models.rag import BaseRAG
from RAG.utils import retrieve_from_vstore, query_llm, chunk_text
from bert_score import score

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
    test_cases = [
        ("We may collect information about your location and device usage to enhance your experience.",
        "The service provider may collect your location data to improve your experience, but they may also use this information for other purposes like targeted ads."),
        
        ("By using our service, you grant us a worldwide, non-exclusive, royalty-free license to use, reproduce, and distribute your user-generated content.",
        "This service can use and share you content worldwide without paying you, which may raise concerns about ownership and compensation."),
        
        ("We reserve the right to terminate your account at any time for any reason without notice.",
        "The company has the power to end you account without notice or explanation, which could ead to loss of access and data."),
        
        ("Your personal information may be shared with our affiliates and partners for marketing purposes.",
        "Your data may be used for targeted ads, potentially without your direct consent, and shared with unknown third parties."),
        
        ("We may modify these terms at any time, and your continued use of the service constitutes acceptance of the changes.",
        "This means the compnay can change its rules without your explicit consent, and contued use implies agreement to new terms."),
        
        ("In the event of a dispute, you agree to resolve the issue through binding arbitration rather than in court.",
        "You may be giving up your right to a court trial if a dispute arises, and instead, a neutral third party will make a decision."),
        
        ("We use cookies and similar technologies to track your activity on our site and other sites.",
        "The company uses technologies to monitor what you do on their site and potentially on other websites too. This extensive tracking could raise privacy concerns."),
        
        ("You are responsible for maintaining the confidentiality of your account information and password.",
        "You need to keep your account details and password secret. While this is standard, it means the company might not help you if your account is compromised due to your own negligence."),
        
        ("We may use your name and profile picture in connection with commercial or sponsored content.",
        "The company might use your name and picture for ads or sponsored posts. This could mean your identity is used to promote products or services without your explicit consent for each use."),
        
        ("By submitting ideas or feedback, you grant us the right to use them without compensation or attribution.",
        "If you give the company ideas or feedback, they can use them for free without giving you credit or payment. This means you could potentially lose out on valuable ideas you share."),
        
        ("All of Your uses of the Netflix Brand Assets in any of Your marketing, advertising, content, or other material (""Your Materials"") are subject to Netflix's approval prior to use.",
         "You must ask permission and get the consent of Netflix before using any of their assets and branding in your marketing or content. This could limit your creative freedom and require extra steps before you can use their materials."),
        
        ("You acknowledge and agree to provide public-facing contact information, a refund policy and order fulfilment timelines on your Shopify Store.", 
         "This company requires you to share your contact details and refund policy on your Shopify store."),
    ]
    F1_corrective, F1_rag = benchmark_models(test_cases)
    print('F1 Score for Corrective RAG: ', F1_corrective)
    print('F1 Score for Base RAG: ', F1_rag)