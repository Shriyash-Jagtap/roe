import requests
import sys
import os

def test_captcha_endpoint(image_path, api_url="http://localhost:8000/captcha"):
    """
    Test the captcha endpoint with an image file
    
    Args:
        image_path: Path to the image file
        api_url: URL of the API endpoint
    
    Returns:
        The response from the API
    """
    if not os.path.exists(image_path):
        print(f"Error: Image file not found at {image_path}")
        return None
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(api_url, files=files)
        
        if response.status_code == 200:
            print("Success! API response:")
            print(response.json())
            return response.json()
        else:
            print(f"Error: API returned status code {response.status_code}")
            print(response.text)
            return None
    
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_api.py <path_to_image>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    test_captcha_endpoint(image_path) 