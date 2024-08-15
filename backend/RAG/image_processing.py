from flask import current_app
import easyocr
import io
from pdf2image import convert_from_bytes
import ssl
import traceback
import numpy as np
from PIL import Image
import os
import urllib.request
import certifi

MODEL_DIR = os.path.join(os.path.dirname(__file__), '../model_storage')

def extract_image_text(file):
    
    # we will be storing the ocr model in the directory instead of locally
    def create_ssl_context():
        return ssl.create_default_context(cafile=certifi.where())
    
    try:
        filename = file.filename.lower()
        print(f"Processing file: {filename}") 
        
        # Check if the model files exist
        model_files = ['craft_mlt_25k.pth', 'english_g2.pth']
        models_exist = all(os.path.exists(os.path.join(MODEL_DIR, f)) for f in model_files)
        
        if not models_exist:
            print("Models not found. Downloading...")
            os.makedirs(MODEL_DIR, exist_ok=True)
            
            ssl_context = create_ssl_context()
            
            # Use the custom SSL context for downloading
            opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_context))
            urllib.request.install_opener(opener)
        
        # initialize ocr and process images
        reader = easyocr.Reader(['en'], model_storage_directory=MODEL_DIR)
        
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            image_bytes = file.read()
            print("Image bytes read successfully") 
            
            image = Image.open(io.BytesIO(image_bytes))
            image_np = np.array(image)
            
            results = reader.readtext(image_np)
            print(f"Results from OCR: {results}") 
            text = ' '.join([res[1] for res in results])
            print("Extracted text from image: ", text)
            return text
        
        elif filename.endswith('.pdf'):
            pdf_bytes = file.read()
            images = convert_from_bytes(pdf_bytes)
            print(f"Converted PDF to {len(images)} images")
            text = ""
            
            for i, image in enumerate(images):
                image_np = np.array(image)
                results = reader.readtext(image_np)
                print(f"Results from OCR on page {i + 1}: {results}") 
                page_text = ' '.join([res[1] for res in results])
                text += f"Page {i + 1}: \n{page_text}\n"
            
            print("Extracted text from PDF: ", text)
            return text
        
        else:
            raise ValueError("Unsupported file type")
    
    except Exception as e:
        current_app.logger.error(f"Error extracting text from image: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        return None