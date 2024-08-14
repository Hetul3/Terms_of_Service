from flask import current_app
import easyocr
import io
from pdf2image import convert_from_bytes
import ssl
import traceback
import numpy as np
from PIL import Image

def extract_image_text(file):
    try:
        filename = file.filename.lower()
        print(f"Processing file: {filename}") 
        
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            reader = easyocr.Reader(['en'])
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
            reader = easyocr.Reader(['en'])
            
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