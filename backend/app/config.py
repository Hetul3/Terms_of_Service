import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    COLLECTION_NAME = os.getenv('COLLECTION_NAME')
    GROQ_KEY = os.getenv('GROQ_KEY')