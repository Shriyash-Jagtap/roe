from fastapi import FastAPI, File, UploadFile, HTTPException
import cv2
import numpy as np
import pytesseract
import re
from io import BytesIO
from PIL import Image

# Set the path to tesseract executable
# You need to change this to your Tesseract installation path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = FastAPI()

@app.post("/captcha")
async def solve_captcha(file: UploadFile = File(...)):
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Read the image
    contents = await file.read()
    image = Image.open(BytesIO(contents))
    
    # Convert to OpenCV format
    image = np.array(image)
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding to enhance text
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    
    # Extract text from the image with different configurations
    # Try different configs to improve OCR accuracy
    configs = [
        '--psm 6',  # Assume a single uniform block of text
        '--psm 11',  # Sparse text. Find as much text as possible without assuming a particular structure
        '--psm 3',   # Fully automatic page segmentation, but no OSD (default)
    ]
    
    text = None
    for config in configs:
        text = pytesseract.image_to_string(thresh, config=config)
        # Try to find multiplication pattern
        multiplication_pattern = r'(\d+)\s*[xX*×]\s*(\d+)'
        match = re.search(multiplication_pattern, text)
        if match:
            break
    
    # If no match found in any configuration
    if not match:
        # Try a more aggressive approach - look for any sequence of digits
        digits = re.findall(r'\d+', text)
        if len(digits) >= 2:
            # Assume the first two sequences of digits are our numbers
            return {
                "answer": int(digits[0]) * int(digits[1]),
                "email": "22f3000165@ds.study.iitm.ac.in"
            }
        
        raise HTTPException(status_code=400, detail="Could not detect multiplication problem in the image")
    
    # Extract the numbers
    num1 = int(match.group(1))
    num2 = int(match.group(2))
    
    # Calculate the result
    result = num1 * num2
    
    # Return the result in the required format
    return {
        "answer": result,
        "email": "22f3000165@ds.study.iitm.ac.in"
    }

@app.get("/")
async def root():
    return {"message": "Welcome to the CAPTCHA solver API. Use POST /captcha to solve multiplication problems."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 