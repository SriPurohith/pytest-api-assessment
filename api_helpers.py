import requests
import os
import logging
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")

logger = logging.getLogger(__name__)
logger.info(f"API Base URL: {BASE_URL}")

# GET requests
def get_api_data(endpoint, params={}):
    # 1. Strip any trailing comments or whitespace from BASE_URL
    clean_base = BASE_URL.split('#')[0].strip().rstrip('/')
    
    # 2. Ensure the endpoint is clean (singular /pet)
    clean_endpoint = endpoint.lstrip('/')
    
    # 3. Combine them
    full_url = f"{clean_base}/{clean_endpoint}"
    
    response = requests.get(full_url, params=params)
    return response

# POST requests
def post_api_data(endpoint, data):
    # Use uppercase BASE_URL here
    response = requests.post(f'{BASE_URL}{endpoint}', json=data)
    return response

# PATCH requests
def patch_api_data(endpoint, data):
    # Use uppercase BASE_URL here
    response = requests.patch(f'{BASE_URL}{endpoint}', json=data, timeout=10)
    return response

# DELETE requests
def delete_api_data(endpoint):
    # Use uppercase BASE_URL here
    url = f"{BASE_URL}{endpoint}"
    response = requests.delete(url)
    print(f"DELETE Request sent to: {url} | Status Code: {response.status_code}")
    return response