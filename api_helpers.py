import requests

base_url = 'http://localhost:5000'

import os
from dotenv import load_dotenv

load_dotenv()

# The order of priority: 
# 1. Environment Variable (from GitHub Secrets or local shell)
# 2. .env file
# 3. Hardcoded default (last resort)
BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")

# Pro-tip: Log the URL once during setup so you can see it in the Action logs
import logging
logger = logging.getLogger(__name__)
logger.info(f"API Base URL: {BASE_URL}")


# GET requests
def get_api_data(endpoint, params = {}):
    response = requests.get(f'{base_url}{endpoint}', params=params)
    return response

# POST requests
def post_api_data(endpoint, data):
    response = requests.post(f'{base_url}{endpoint}', json=data)
    return response


# PATCH requests
def patch_api_data(endpoint, data):
    response = requests.patch(f'{base_url}{endpoint}', json=data)
    return response

# DELETE requests (added)
def delete_api_data(endpoint):
    url = f"{base_url}{endpoint}"
    response = requests.delete(url)
    
    # Log the action for debugging (useful when running with -s)
    print(f"DELETE Request sent to: {url} | Status Code: {response.status_code}")
    return response