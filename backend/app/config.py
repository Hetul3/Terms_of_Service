import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    COLLECTION_NAME = os.getenv('COLLECTION_NAME')
    GROQ_KEY = os.getenv('GROQ_KEY')
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    TABLE_NAME = os.getenv('TABLE_NAME')