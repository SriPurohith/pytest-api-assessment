# Standard library
import json
from jsonschema import validate
from urllib import response

# Third-party
import pytest

# Local modules
import schemas
import api_helpers

# ---------------------------------------------------------
# TEST CASE: test pet schema
# ---------------------------------------------------------
def test_pet_schema():
    test_endpoint = "/pets/1"

    response = api_helpers.get_api_data(test_endpoint)

    assert response.status_code == 200

    # Validate the response schema against the defined schema in schemas.py
    validate(instance=response.json(), schema=schemas.pet)


# ---------------------------------------------------------
# TEST CASE: test status code (200) and response content
# ---------------------------------------------------------
@pytest.mark.parametrize("status", [
    "available", #available status
    "pending", #pending status
    "sold" #sold status
    ])

def test_find_by_status_200(status):
    test_endpoint = "/pets/findByStatus"
    params = {
        "status": status
    }

    response = api_helpers.get_api_data(test_endpoint, params)
    
    # Displaying the response details for debugging purposes
    print(f"\n\nStatus: {response.status_code}", flush=True)
    print(f"Header: {response.headers}", flush=True)
    print(f"Json: {response.json()}", flush=True)
    print(f"No of pets: {len(response.json())}", flush=True)

    # Validating Status Code
    assert response.status_code == 200

    # Validating Content Type
    assert response.headers["Content-Type"] == "application/json"

    # Validating Response Body is a List
    response_data = response.json()
    assert isinstance(response_data, list)

    # Verifying that the Schema of the first item is valid if the list not empty
    if len(response_data) > 0:
        import schemas
        from jsonschema import validate
        #Comparing with the defined schema in schemas.py
        validate(instance=response_data[0], schema=schemas.pet)


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
    "9223372036854775807",   
    "🐶",                       
    "1e10",
    #--- Valid but Non-Existent IDs ---
    5555
])

def test_get_by_id_404(pet_id):
    test_endpoint = f"/pets/{pet_id}"
    payload = api_helpers.get_api_data(test_endpoint)

    # Validating status code is 404 for non-existent (NOT FOUND) pet IDs
    assert payload.status_code == 404

    # Trying to parse json if the response actually is json
    if "application/json" in payload.headers.get("Content-Type", ""):
        payload_data = payload.json()
        assert "not found" in payload_data.get("message", "").lower()
    else:
        print(f"Verified: ID {pet_id} returned a 404 HTML page.")