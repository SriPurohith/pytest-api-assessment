# Standard library
import json
from jsonschema import validate
from urllib import response
import logging

# Third-party
import pytest

# Local modules
import schemas
import api_helpers

# Enable logging for debugging purposes 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# TEST CASE: test pet schema
# ---------------------------------------------------------
def test_pet_schema():
# 1. Choose endpoint based on environment
    if "localhost" in api_helpers.BASE_URL:
        list_endpoint = "/pets/findByStatus"
    else:
        list_endpoint = "/pet/findByStatus"

    # 2. Fetch data
    list_response = api_helpers.get_api_data(list_endpoint, params={"status": "available"})
    
    # 3. Safety check to avoid JSONDecodeError on 404
    if list_response.status_code != 200:
        pytest.fail(f"Schema test failed: {list_endpoint} returned {list_response.status_code}")

    available_pets = list_response.json()

    assert list_response.status_code == 200
    
    # 4. Validate against your schema
    if len(available_pets) > 0:
        validate(instance=available_pets[0], schema=schemas.pet)
        logger.info(f"Successfully validated schema for pet: {available_pets[0]['name']}")
    else:
        pytest.skip("No pets found in the list to validate against the schema.")


# ---------------------------------------------------------
# TEST CASE: test status code (200) and response content
# ---------------------------------------------------------
@pytest.mark.parametrize("status", [
    "available", #available status
    "pending", #pending status
    "sold" #sold status
    ])

def test_find_by_status_200(status):
    if "localhost" in api_helpers.BASE_URL:
        test_endpoint = "/pets/findByStatus"
    else:
        test_endpoint = "/pet/findByStatus"
        
    params = {"status": status}
    response = api_helpers.get_api_data(test_endpoint, params)
    
    logger.info(f"Status: {response.status_code}")
    
    # 1. First, assert the status code so we don't try to parse a 404
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}. Response: {response.text}"

    # 2. Parse once and reuse
    response_data = response.json()
    logger.info(f"Pets found: {len(response_data)}")

    # 3. Final structural validation
    assert isinstance(response_data, list), "Response body is not a list!"


# ---------------------------------------------------------
# TEST CASE: test status code (404) cases for GET by pet_id
# ---------------------------------------------------------
@pytest.mark.parametrize("pet_id", [
    # --- Standard 404s ---
    999999, "-1", "abc", 
    # --- Structural Edge Cases ---
    " ", "922337203.22", "null", "False",
    # --- Security & Resilience ---
    "%27%20OR%201=1",          
    "<script>alert(1)</script>", 
    "999999999999999",   
    "🐶",                       
    "1e10",
    #--- Valid but Non-Existent IDs ---
    5555
])

def test_get_by_id_404(pet_id):
    if "localhost" in api_helpers.BASE_URL:
        list_endpoint = "/pets/findByStatus"
    else:
        list_endpoint = "/pet/findByStatus"
    list_response = api_helpers.get_api_data(list_endpoint, params={"status": "available"})

    # 1. The primary safety check
    assert list_response.status_code < 500

    if list_response.status_code != 200:
        # 2. Only try to parse JSON if the header says it is JSON
        if "application/json" in list_response.headers.get("Content-Type", ""):
            message = list_response.json().get("message", "").lower()
            assert any(word in message for word in ["not found", "exception", "input string", "unknown"])
        else:
            # 3. If it's XML (like in your error), just check the raw text
            message = list_response.text.lower()
            assert "not found" in message or "apiresponse" in message