import pytest
from unittest.mock import patch, MagicMock
import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from RAG.RAG_Models.dynamic_corrective_rag import CorrectiveRAG
from RAG.llm import retrieve_from_vstore, query_llm, chunk_text

@pytest.fixture
def corrective_rag(generator_models, reasoning_models):
    return CorrectiveRAG(generator_models, reasoning_models)
    
def test_classify_prompt_text(corrective_rag):
    assert corrective_rag.classify_prompt_text("We will not use cookies to collect personally identifiable information about visitors. We will not share any information we collect with anyone outside of the National Archives. The usage of cookies in this way is considered a """"Tier 2"""" under the Office of Management and Budget's Memorandum 10-22, Guidance for Online Use of Web Measurement and Customization Technologies. If you wish to disable cookies and opt out of this process, you can find opt-out instructions on usa.gov. Disabling cookies will not restrict your access to the core content of the website.") == 0.742

def test_determine_text_classification(corrective_rag):
    prompt_text = "Netflix grants You a limited, non-exclusive, revocable, non-sublicensable and non-transferable license to display the Netflix Brand Assets in accordance with these Terms."
    retrieval_results = retrieve_from_vstore(prompt_text, ['metadatas', 'documents', 'distances'])
    doc = retrieval_results['documents'][0][0]
    cosine_similarity = retrieval_results['distances'][0][0]
    metadata = retrieval_results['metadatas'][0][0]
    print(corrective_rag.determine_text_classification(cosine_similarity, doc, prompt_text, 0.35))
    relation, score = corrective_rag.determine_text_classification(cosine_similarity, doc, prompt_text, 0.35)
    assert relation == 'related'
    
def test_process_text(corrective_rag):
    chunk = "Netflix grants You a limited, non-exclusive, revocable, non-sublicensable and non-transferable license to display the Netflix Brand Assets in accordance with these Terms."
    print("results: ", corrective_rag.process_text(chunk))
    assert True
    
def test_process_result_object(corrective_rag):
    sample_results = [
        {
            'chunk': 'Netflix grants You a limited, non-exclusive, revocable, non-sublicensable and non-transferable license to display the Netflix Brand Assets in accordance with these Terms.',
            'document': 'Any Content you submit will be considered to be non-proprietary and non-confidential.',
            'relation': 'semi-related',
            'classification': ['First Party Collection/Use', 'Introductory/Generic', 'Practice not covered', 'Third Party Sharing/Collection'],
            'refinement': None,
            'distance': 0.35152671014875164
        },
        {
            'chunk': 'Netflix grants You a limited, non-exclusive, revocable, non-sublicensable and non-transferable license to display the Netflix Brand Assets in accordance with these Terms.',
            'document': 'If you link your account with us to your UltraViolet account, we may collect information regarding UltraViolet-enabled movies and television shows you have purchased from third party retailers. This will enable you to download or stream movies or television shows from us that you have purchased from us from such third parties. For more information, please view the UltraViolet privacy policy.',
            'relation': 'semi-related',
            'classification': ['First Party Collection/Use'],
            'refinement': None,
            'distance': 0.3550540328025818
        },
        {
            'chunk': 'Netflix grants You a limited, non-exclusive, revocable, non-sublicensable and non-transferable license to display the Netflix Brand Assets in accordance with these Terms.',
            'document': '(e) Subscription Video Services. We may offer the right for you to access video content as a paid subscription service("Paid Video Subscription Services"). As a condition of becoming a subscriber, you must grant your consent to allow us to share information about the content you have viewed to third parties in order to provide you with the service, for our and others\' marketing purposes and to help you inform others about your experiences on social media services such as Facebook and Twitter. If you no longer wish us to share information about what you have watched on our service, you can cancel your subscription at any time. A list of those Paid Video Subscription Services, together with information on how to contact customer service about your account, will appear here. Current Paid Video Subscription Services are: Cosmobody - service@cosmobody.com',
            'relation': 'semi-related',
            'classification': ['Privacy contact information', 'User Choice/Control', 'Third Party Sharing/Collection'],
            'refinement': None,
            'distance': 0.47346036434173583
        }
    ]

    expected_output = {
        'Netflix grants You a limited, non-exclusive, revocable, non-sublicensable and non-transferable license to display the Netflix Brand Assets in accordance with these Terms.': [
            {
                'document': 'Any Content you submit will be considered to be non-proprietary and non-confidential.',
                'relation': 'semi-related',
                'classification': ['First Party Collection/Use', 'Introductory/Generic', 'Practice not covered', 'Third Party Sharing/Collection'],
                'refinement': None,
                'distance': 0.35152671014875164
            },
            {
                'document': 'If you link your account with us to your UltraViolet account, we may collect information regarding UltraViolet-enabled movies and television shows you have purchased from third party retailers. This will enable you to download or stream movies or television shows from us that you have purchased from us from such third parties. For more information, please view the UltraViolet privacy policy.',
                'relation': 'semi-related',
                'classification': ['First Party Collection/Use'],
                'refinement': None,
                'distance': 0.3550540328025818
            },
            {
                'document': '(e) Subscription Video Services. We may offer the right for you to access video content as a paid subscription service("Paid Video Subscription Services"). As a condition of becoming a subscriber, you must grant your consent to allow us to share information about the content you have viewed to third parties in order to provide you with the service, for our and others\' marketing purposes and to help you inform others about your experiences on social media services such as Facebook and Twitter. If you no longer wish us to share information about what you have watched on our service, you can cancel your subscription at any time. A list of those Paid Video Subscription Services, together with information on how to contact customer service about your account, will appear here. Current Paid Video Subscription Services are: Cosmobody - service@cosmobody.com',
                'relation': 'semi-related',
                'classification': ['Privacy contact information', 'User Choice/Control', 'Third Party Sharing/Collection'],
                'refinement': None,
                'distance': 0.47346036434173583
            }
        ]
    }

    result = corrective_rag.process_result_object(sample_results)
    assert result == expected_output, f"Expected {expected_output}, but got {result}"
    
def test_generate_explanations(corrective_rag):
    input = {
        'Netflix grants You a limited, non-exclusive, revocable, non-sublicensable and non-transferable license to display the Netflix Brand Assets in accordance with these Terms.': [
            {
                'document': 'Any Content you submit will be considered to be non-proprietary and non-confidential.',
                'relation': 'semi-related',
                'classification': ['First Party Collection/Use', 'Introductory/Generic', 'Practice not covered', 'Third Party Sharing/Collection'],
                'refinement': None,
                'distance': 0.35152671014875164
            },
            {
                'document': 'If you link your account with us to your UltraViolet account, we may collect information regarding UltraViolet-enabled movies and television shows you have purchased from third party retailers. This will enable you to download or stream movies or television shows from us that you have purchased from us from such third parties. For more information, please view the UltraViolet privacy policy.',
                'relation': 'semi-related',
                'classification': ['First Party Collection/Use'],
                'refinement': None,
                'distance': 0.3550540328025818
            },
            {
                'document': '(e) Subscription Video Services. We may offer the right for you to access video content as a paid subscription service("Paid Video Subscription Services"). As a condition of becoming a subscriber, you must grant your consent to allow us to share information about the content you have viewed to third parties in order to provide you with the service, for our and others\' marketing purposes and to help you inform others about your experiences on social media services such as Facebook and Twitter. If you no longer wish us to share information about what you have watched on our service, you can cancel your subscription at any time. A list of those Paid Video Subscription Services, together with information on how to contact customer service about your account, will appear here. Current Paid Video Subscription Services are: Cosmobody - service@cosmobody.com',
                'relation': 'related',
                'classification': ['Privacy contact information', 'User Choice/Control', 'Third Party Sharing/Collection'],
                'refinement': None,
                'distance': 0.47346036434173583
            }
        ]
    }
    
    print("explanations: ", corrective_rag.generate_explanations(input))
    # since the outputs can be variable, if it outputs anything without erorr then the test passes
    assert True
    
