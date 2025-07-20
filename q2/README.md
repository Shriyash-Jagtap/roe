# CAPTCHA Solver API

This FastAPI application processes images containing multiplication problems, extracts the numbers, calculates the result, and returns the answer in JSON format.

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn
- Python-multipart
- PyTesseract
- OpenCV
- NumPy
- Tesseract OCR (external dependency)

## Installation

1. Install Python dependencies:
```
pip install fastapi uvicorn python-multipart pytesseract opencv-python numpy
```

2. Install Tesseract OCR:
   - Windows: Download and install from https://github.com/UB-Mannheim/tesseract/wiki
   - Linux: `sudo apt install tesseract-ocr`
   - macOS: `brew install tesseract`

3. Update the Tesseract path in `main.py` if necessary:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows path
# For Linux/macOS, this line can be removed as pytesseract will find the installation automatically
```

## Running the API

Start the server with:
```
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

## Endpoints

### POST /captcha

Upload an image containing a multiplication problem.

**Request:**
- Method: POST
- URL: `/captcha`
- Body: Form data with a file field named "file"

**Response:**
```json
{
  "answer": 12345678,
  "email": "22f3000165@ds.study.iitm.ac.in"
}
```

### GET /

Welcome message and basic instructions.

## Testing

You can test the API using curl:
```
curl -X POST -F "file=@path/to/your/image.jpg" http://localhost:8000/captcha
```

Or using the interactive API documentation at http://localhost:8000/docs 