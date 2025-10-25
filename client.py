import httpx
import base64


def get_client_data(url: str, username: str, password: str) -> dict:
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {"Authorization": f"Basic {encoded_credentials}"}

    response = httpx.get(url, headers=headers, timeout=5.0)
    response.raise_for_status()
    return response.json()


def get_python_version_from_pypi(package_name: str, version: str) -> str:
    pypi_url = f"https://pypi.org/pypi/{package_name}/{version}/json"
    print(f"PyPI Url is: https://pypi.org/pypi/{package_name}/{version}/json")
    response = httpx.get(pypi_url, timeout=5.0)
    response.raise_for_status()
    return response.json()["info"]["requires_python"]


def main():
    try:
        data = get_client_data("http://localhost:8000/", "user", "password")
        client_info = data["iqm_client"]
        version = get_python_version_from_pypi(
            client_info["package_name"], client_info["min"]
        )
        print(f"Minimum Python version: {version}", "✅")
    except httpx.HTTPStatusError as e:
        print(f"HTTP error {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        print(f"Network error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
