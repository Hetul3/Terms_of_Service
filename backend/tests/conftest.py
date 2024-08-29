import pytest
import os
from dotenv import load_dotenv


@pytest.fixture(scope='module')
def generator_models():
    """Ficture to provide generator models for testing"""
    return ['llama-3.1-70b-versatile', 'llama3-70b-8192', 'llama3-groq-70b-8192-tool-use-preview']

@pytest.fixture(scope='module')
def reasoning_models():
    """Fixture to provide reasoning models for testing"""
    return ['llama-3.1-8b-instant', 'llama3-8b-8192', 'mixtral-8x7b-32768', 'gemma2-9b-it']
