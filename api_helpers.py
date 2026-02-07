import requests
import os
import logging
from dotenv import load_dotenv

load_dotenv()

# BASE_URL is now uppercase to match usage in api_helpers and avoid confusion with the local variable in the fixture.
BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")

logger = logging.getLogger(__name__)
logger.info(f"API Base URL: {BASE_URL}")

# GET requests
def get_api_data(endpoint, params={}):
    # Cleaning up the BASE_URL in case there are comments or extra slashes in the .env
    clean_base = BASE_URL.split('#')[0].strip().rstrip('/')
    clean_endpoint = endpoint.lstrip('/')
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