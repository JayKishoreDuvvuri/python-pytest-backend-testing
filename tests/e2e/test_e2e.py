# End-to-End Test Cases:
# E2E Test Case 1, E2E Test Case 2 and E2E Test Case 3

import json
import httpx
import pytest
from client import get_client_data
import asyncio

BASE_URL = "http://localhost:8000"
AUTH = ("user", "password")


@pytest.mark.asyncio
async def test_get_all_clients_from_fastapi():
    """
    E2E Test Case 1:
    Scenario: Request all client metadata from FastAPI through NGINX

    Description:
    This test checks if the FastAPI server correctly returns all available client metadata when accessed at the root endpoint (/).
    It also verifies that the response:
           * Has HTTP 200 status code
           * Includes expected keys (iqm_client and its package_name)
           * Matches exactly with the expected data defined in data.json

    Purpose:
    To ensure the FastAPI server returns the full and correct client metadata structure as configured.
    """
    async with httpx.AsyncClient(base_url=BASE_URL, auth=AUTH) as client:
        # Load the expected data from data.json
        with open("data.json") as f:
            expected_data = json.load(f)

            response = await client.get("/")
            assert response.status_code == 200

            data = response.json()

            # Basic Assertion
            assert "iqm_client" in data
            assert "package_name" in data["iqm_client"]

            # Full document validation
            assert data == expected_data, (
                "\nJSON response does not match data.json"
                f"\nExpected:\n{json.dumps(expected_data, indent=2)}"
                f"\nGot:\n{json.dumps(data, indent=2)}"
            )
            print("\n Full JSON Document:\n", json.dumps(data, indent=2), "✅")
            print("\n All clients fetched successfully.", "✅")


@pytest.mark.asyncio
async def test_get_specific_client_metadata():
    """
    E2E Test Case 2:
    Scenario: Request only specific client (iqm_calibration)

    Description:
    This test queries the FastAPI server with a specific query parameter: client_key=iqm_calibration.
    It checks that:
          * The response returns only one client (iqm_calibration)
          * That client's package_name is correctly returned as "iqm-calibration"

    Purpose:
    To validate the server's ability to filter and return metadata for a single, specified client.
    """
    async with httpx.AsyncClient(base_url=BASE_URL, auth=AUTH) as client:
        response = await client.get("/", params={"client_key": "iqm_calibration"})
        assert response.status_code == 200

        data = response.json()
        assert list(data.keys()) == ["iqm_calibration"]
        assert data["iqm_calibration"]["package_name"] == "iqm-calibration"
        print(
            "\n Specific client metadata (iqm_calibration) fetched successfully.", "✅"
        )


def test_client_fastapi_interaction():
    """
    E2E Test Case 3:
    Scenario: client.py fetches metadata from FastAPI

    Description:
    This is an end-to-end (E2E) test that imports and calls the get_client_data() function
    from client.py to interact with the FastAPI backend. It ensures the function:
           * Connects to the server
           * Authenticates properly
           * Retrieves a dictionary with the correct structure (e.g., key iqm_client with subkey package_name)

    Purpose:
    To verify that the client script logic works end-to-end with the actual
    FastAPI server — including HTTP request, authentication, and JSON parsing.
    """
    data = get_client_data(BASE_URL, *AUTH)

    assert "iqm_client" in data
    assert "package_name" in data["iqm_client"]

    print("\n client.py successfully fetched metadata from FastAPI.", "✅")
