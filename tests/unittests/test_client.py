# Unit Test Cases for client.py
# Unit Test Case 1 and Unit Test Case 2

import httpx
from unittest.mock import patch, Mock
from client import get_client_data, get_python_version_from_pypi


def test_get_client_data():
    """
    Unit Test Case 1:
    Scenario: Mock response from API (Main.py - FastAPI Backend)

    Description:
    Verifies that `get_client_data()` correctly parses and returns client metadata
    fetched from the FastAPI backend (mocked).

    Purpose:
    The test mocks the `httpx.get` response to simulate the API returning a JSON
    payload with package name and minimum version, then checks that the function
    correctly extracts these fields.
    """
    mock_client_response = Mock()
    mock_client_response.raise_for_status = Mock()
    mock_client_response.json.return_value = {
        "client": {"package_name": "iqm-calibration", "min": "4.1"}
    }

    with patch("httpx.get", return_value=mock_client_response):
        client_data = get_client_data("http://localhost:8000/", "user", "password")
        print(
            "\n Client name and Client package name is:",
            client_data["client"]["package_name"],
        )
        print("Client data for Min:", client_data["client"]["min"])
        assert client_data["client"]["package_name"] == "iqm-calibration"
        assert client_data["client"]["min"] == "4.1"


def test_get_python_version_from_pypi():
    """
    Unit Test Case 2:
    Scenario: # Mock response from PyPI API

    Description:
    Verifies that `get_python_version_from_pypi()` correctly retrieves
    and returns the required Python version from the PyPI JSON response (mocked).

    Purpose:
    The test mocks `httpx.get` to simulate a PyPI API call for a specific package version,
    and checks if the function correctly reads the `requires_python` value.
    """
    mock_pypi_response = Mock()
    mock_pypi_response.raise_for_status = Mock()
    mock_pypi_response.json.return_value = {"info": {"requires_python": ">=3.8"}}

    with patch("httpx.get", return_value=mock_pypi_response):
        python_version = get_python_version_from_pypi("iqm_client", "13.2")
        print("\n Python version is:", python_version)
        assert python_version == ">=3.8"
