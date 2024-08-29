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