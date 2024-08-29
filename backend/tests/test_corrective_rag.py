import pytest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from RAG.RAG_Models.dynamic_corrective_rag import CorrectiveRAG

@pytest.fixture
def corrective_rag(generator_models, reasoning_models):
    return CorrectiveRAG(generator_models, reasoning_models)

def test_testing_function(corrective_rag):
    assert CorrectiveRAG.testing() == "testing works"
    
def test_classify_prompt_text(corrective_rag):
    assert corrective_rag.classify_prompt_text("We will not use cookies to collect personally identifiable information about visitors. We will not share any information we collect with anyone outside of the National Archives. The usage of cookies in this way is considered a """"Tier 2"""" under the Office of Management and Budget's Memorandum 10-22, Guidance for Online Use of Web Measurement and Customization Technologies. If you wish to disable cookies and opt out of this process, you can find opt-out instructions on usa.gov. Disabling cookies will not restrict your access to the core content of the website.") == 0.742