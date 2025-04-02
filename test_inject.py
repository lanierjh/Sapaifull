import requests
from urllib.parse import urljoin
import json
import webbrowser
import time

def test_inject():
    # First, open the main page in a browser
    main_url = "http://127.0.0.1:5500/sapai-extension/index.html"
    print(f"Opening main page: {main_url}")
    webbrowser.open(main_url)
    
    # Wait a moment for the page to load
    print("Waiting for page to load...")
    time.sleep(2)
    
    # The URL where your React app is running
    base_url = "http://127.0.0.1:5500"
    
    # JavaScript code to execute
    js_code = 'window.receiveMessage("Test message from Python script");'
    
    # Full URL
    full_url = urljoin(base_url, "/sapai-extension/inject.html")
    print(f"Sending request to: {full_url}")
    
    # Send the request
    try:
        response = requests.get(
            full_url,
            params={"js": js_code}
        )
        
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.text[:100]}...")
        
        if response.status_code == 200:
            print("Request successful!")
        else:
            print(f"Request failed with status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending request: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_inject() 