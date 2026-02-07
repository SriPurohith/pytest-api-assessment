# Standard library
import json
from jsonschema import validate
import threading
import logging

# Third-party
import pytest

# Local modules
import schemas
import api_helpers

# Using a lock here just in case we run these tests in parallel.
# Don't want two tests trying to seed/grab the same ID at the exact same millisecond.
data_lock = threading.Lock()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# Fixtures: Handling dynamic setup and test data
# ---------------------------------------------------------
@pytest.fixture(scope="session") 
def available_pet_id(): 
    with data_lock:
        try:
            # The local mock provided uses plural (/pets), but public Swagger uses singular (/pet).
            # This check keeps the suite from 404 errors when switching between the envs.
            if "localhost" in api_helpers.BASE_URL:
                endpoint = "/pets/findByStatus"
            else:
                endpoint = "/pet/findByStatus"
            response = api_helpers.get_api_data(endpoint, params={"status": "available"})
            logger.info(f"Connected to {response.url} | Status: {response.status_code}")
        except Exception as e:
            pytest.skip(f"Connection Error: {e}")

        if response.status_code != 200:
            pytest.skip(f"Server returned {response.status_code} instead of 200")
            
        pets = response.json()
        
        if not pets:
            logger.info("No available pets found, seeding a new pet...")
            seed_payload = {"id": 999, "name": "TestPet", "status": "available"}
            # The local mock provided uses plural (/pets), but public Swagger uses singular (/pet).
            # This check keeps the suite from 404 errors when switching between the envs
            if "localhost" in api_helpers.BASE_URL:
                endpoint = "/pets"
            else:
                endpoint = "/pet"
            api_helpers.post_api_data(endpoint, seed_payload)
            pet_id = 999  # Set the variable instead of returning
        else:
            pet_id = pets[0]['id']
            logger.info(f"Pet ID: {pet_id} selected for testing.")

    # Providing the pet_id to the test
    yield pet_id

@pytest.fixture(scope="function") #Create an order for the available pet and return the order ID (UUID)
def created_order_id(available_pet_id):
    # --- SETUP: Creating the entry ---
    create_payload = {"pet_id": available_pet_id, "status": "available"}
    res = api_helpers.post_api_data("/store/order", create_payload)
    
    if res.status_code not in [200, 201]:
        pytest.fail(f"Setup failed: {res.text}")
        
    order_id = res.json().get("id")
    logger.info(f"Order ID: {order_id} created for testing.")

    # Providing the ID to the test
    yield order_id

    # --- tearingdown ---
    logger.info(f"\nCleaning up: Deleting order {order_id}")
    delete_res = api_helpers.delete_api_data(f"/store/order/{order_id}")

    # Some environments don't like DELETE requests on these IDs. 
    # Warning instead of failing so the whole test doesn't tank during cleanup. 
    if delete_res.status_code == 405:
        logger.warning(f"Server does not support DELETE on this endpoint (405). Manual cleanup may be required.")
    else:
        assert delete_res.status_code == 200, f"Cleanup failed for ID {order_id}"

    
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
@pytest.mark.flaky(reruns=2, reruns_delay=1)
def test_patch_order_by_id(created_order_id, update_payload):
    endpoint = f"/store/order/{created_order_id}" 
    
    response = api_helpers.patch_api_data(endpoint, update_payload)

    # Public Swagger doesn't support PATCH on orders (returns 405), 
    # but I kept the 200 check for the local mock as per the TODO.
    if "petstore.swagger.io" in api_helpers.BASE_URL:
        assert response.status_code == 405
        logger.info("Public API correctly rejected PATCH (as expected).")
    else:
        assert response.status_code == 200
        assert response.json().get("message") == "Order and pet status updated successfully"