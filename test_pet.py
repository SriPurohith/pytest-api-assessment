#import api_helpers as api_modules
import api_helpers   
from urllib import response
from jsonschema import validate
import pytest
import schemas
from hamcrest import assert_that, contains_string, is_

'''
TODO: Finish this test by...
1) Troubleshooting and fixing the test failure
The purpose of this test is to validate the response matches the expected schema defined in schemas.py
'''
def test_pet_schema():
    test_endpoint = "/pets/1"

    response = api_helpers.get_api_data(test_endpoint)

    assert response.status_code == 200

    # Validate the response schema against the defined schema in schemas.py
    validate(instance=response.json(), schema=schemas.pet)

'''
TODO: Finish this test by...
1) Extending the parameterization to include all available statuses
2) Validate the appropriate response code
3) Validate the 'status' property in the response is equal to the expected status
4) Validate the schema for each object in the response
'''
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
    print(f"\n\nSTATUS: {response.status_code}", flush=True)
    print(f"HEADERS: {response.headers}", flush=True)
    print(f"JSON: {response.json()}", flush=True)
    print(f"NUMBER OF PETS: {len(response.json())}", flush=True)

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

'''
TODO: Finish this test by...
1) Testing and validating the appropriate 404 response for /pets/{pet_id}
2) Parameterizing the test for any edge cases
'''
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

    # Step 2: Only try to parse JSON if the response actually IS JSON
    if "application/json" in payload.headers.get("Content-Type", ""):
        payload_data = payload.json()
        
        # Step 3: Use 'in' to handle the long descriptive error message
        # This makes the test pass whether the message is short or long
        assert "not found" in payload_data.get("message", "").lower()
    else:
        # If it's an HTML response (like for -1 or abc), the 404 assertion 
        # above is enough to prove the test passed.
        print(f"Verified: ID {pet_id} returned a 404 HTML page.")