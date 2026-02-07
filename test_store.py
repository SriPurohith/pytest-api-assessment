# Standard library
import json
from jsonschema import validate

# Third-party
import pytest

# Local modules
import schemas
import api_helpers

# ---------------------------------------------------------
# FIXTURES: Handling dynamic setup and test data
# ---------------------------------------------------------
@pytest.fixture #Get the first available pet ID dynamically 
def available_pet_id(): 
    # Use the existing GET helper to find available pets
    response = api_helpers.get_api_data("/pets/findByStatus", params={"status": "available"})
    assert response.status_code == 200
    
    pets = response.json()
    if not pets:
        pytest.skip("No available pets found in the system to run the test.")
    
    # Return the ID of the first available pet found
    return pets[0]["id"]

@pytest.fixture #Create an order for the available pet and return the order ID (UUID)
def created_order_id(available_pet_id):
    create_payload = {"pet_id": available_pet_id, "status": "available"}
    res = api_helpers.post_api_data("/store/order", create_payload)
    
    # Explicitly handling setup failure makes the test results cleaner
    if res.status_code not in [200, 201]:
        pytest.fail(f"Test setup failed: Server returned {res.status_code} during order creation.")
        
    return res.json().get("id")

@pytest.fixture # The payload for the PATCH request, linked to the same pet (dictio)
def update_payload(available_pet_id):
    """The data used to perform the PATCH update, linked to the same pet."""
    return {
        "pet_id": available_pet_id,
        "status": "sold" #changed to sold as per the server's expected values
    }

# ---------------------------------------------------------
# TEST CASE: Patch Order by ID
# ---------------------------------------------------------
def test_patch_order_by_id(created_order_id, update_payload):
    # Performing the PATCH using the dynamic ID and payload from the fixtures
    endpoint = f"/store/order/{created_order_id}"
    response = api_helpers.patch_api_data(endpoint, update_payload)

    # Standard Python assert for the status code
    assert response.status_code == 200, f"Patch failed: {response.text}"
    
    response_data = response.json()

    # Standard Python assert for the message value
    expected_msg = "Order and pet status updated successfully"
    assert response_data["message"] == expected_msg, f"Expected {expected_msg}, but got {response_data.get('message')}"

    # Schema validation
    validate(instance=response_data, schema=schemas.patch_order_response)