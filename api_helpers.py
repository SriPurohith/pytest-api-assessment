import requests

base_url = 'http://localhost:5000'

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

# DELETE requests
def delete_api_data(endpoint):
    """
    Sends a DELETE request to a specific endpoint.
    """
    url = f"{base_url}{endpoint}"
    # Using the 'requests' library to send the DELETE verb
    response = requests.delete(url)
    
    # Log the action for debugging (useful when running with -s)
    print(f"DELETE Request sent to: {url} | Status Code: {response.status_code}")
    return response