# Unit Test Cases for FastApi Server (main.py)
# Unit Test Case 1, Unit Test Case 2, Unit Test Case 3, Unit Test Case 4

from fastapi.testclient import TestClient
from app.main import app
import httpx

client = TestClient(app)


def test_valid_client_key(monkeypatch):
    """
    Unit Test Case 1:
    Scenario: 200 OK - Valid client_key

    Description:
    FastAPI returns valid client metadata when a correct `client_key` is provided.

    Purpose:
    Mocks a successful response from the data service and verifies that FastAPI returns
    the correct metadata with a 200 OK status.
    """

    mock_data = {"iqm_client": {"name": "IQM client", "package_name": "iqm-client"}}

    class MockResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return mock_data

    monkeypatch.setattr(httpx, "get", lambda *args, **kwargs: MockResponse())

    response = client.get("/?client_key=iqm_client")
    print("200 OK Response:", response.json())
    assert response.status_code == 200
    assert response.json() == {"iqm_client": mock_data["iqm_client"]}


def test_request_error(monkeypatch):
    """
    Unit Test Case 2:
    Scenario: 502 - RequestError (Can't connect to data service)

    Description:
    FastAPI handles a connection failure to the data service gracefully.

    Purpose:
    Simulates an `httpx.RequestError` (e.g., connection timeout or DNS failure),
    and ensures FastAPI returns a 502 error with the appropriate error message.
    """

    def mock_get(*args, **kwargs):
        raise httpx.RequestError("Connection failed")

    monkeypatch.setattr(httpx, "get", mock_get)

    response = client.get("/")
    print("502 Connection Failure Response:", response.json())
    assert response.status_code == 502
    assert response.json() == {"detail": "Error connecting to data service"}


def test_http_status_error(monkeypatch):
    """
    Unit Test Case 3:
    Scenario: 502 - HTTPStatusError (e.g. response status != 2xx)

    Description:
    FastAPI returns a 502 error when the data service responds with a non-2xx status.

    Purpose:
    Simulates an `httpx.RequestError` (e.g., connection timeout or DNS failure),
    and ensures FastAPI returns a 502 error with the appropriate error message.
    """

    def mock_get(*args, **kwargs):
        raise httpx.HTTPStatusError("Bad response", request=None, response=None)

    monkeypatch.setattr(httpx, "get", mock_get)

    response = client.get("/")
    print("502 HTTPStatusError Response:", response.json())
    assert response.status_code == 502
    assert response.json() == {"detail": "Invalid response from data service"}


def test_internal_server_error(monkeypatch):
    """
    Unit Test Case 4:
    Scenario: 500 - Internal Server exception

    Description:
    FastAPI returns a 500 error when an unexpected internal exception is raised.

    Purpose:
    Mocks a generic exception (e.g., `ValueError`) during the request handling,
    and checks that FastAPI responds with a 500 status and "Internal Server Error" message.
    """

    def mock_get(*args, **kwargs):
        raise ValueError("Unexpected")

    monkeypatch.setattr(httpx, "get", mock_get)

    response = client.get("/")
    print("500 Internal Server Error Response:", response.json())
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal Server Error"}
