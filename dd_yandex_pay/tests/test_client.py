"""
Cases:
  * Checking default headers.
  * Checking header overrides.
  * Checking custom headers.
  * Using the urllib.parse.urljoin method to form a URL.
  * Using the get_headers method on a request.
 """

from unittest.mock import patch

import requests

from dd_yandex_pay import client


custom_response = requests.Response()
custom_response.status_code = 200


@patch("uuid.uuid4", return_value="7928a3ec-05be-4819-9f80-a757c33293e9")
def test_default_headers(mocked_uuid4):
    """
    Checking default headers.
    """

    yp_client = client.YandexPayClient("api-key", deadline=42000)
    headers = yp_client.get_headers()
    assert headers == {
        "Authorization": "Api-Key api-key",
        "X-Request-Id": "7928a3ec-05be-4819-9f80-a757c33293e9",
        "X-Request-Timeout": "42000",
    }


@patch("uuid.uuid4", return_value="7928a3ec-05be-4819-9f80-a757c33293e9")
def test_override_headers(mocked_uuid4):
    """
    Checking header overrides.
    """

    overided_headers = {
        "Authorization": "Api-Key another-api-key",
        "X-Request-Id": "94c79a87-0e33-4504-a36e-fcdc1be187d1",
        "X-Request-Timeout": "21",
    }

    yp_client = client.YandexPayClient("api-key", deadline=42000)
    headers = yp_client.get_headers(overided_headers)
    assert headers == overided_headers


@patch("uuid.uuid4", return_value="7928a3ec-05be-4819-9f80-a757c33293e9")
def test_custom_headers(mocked_uuid4):
    """
    Checking custom headers.
    """

    yp_client = client.YandexPayClient("api-key", deadline=42000)
    headers = yp_client.get_headers({"X-Authorization": "Bearer auth_key"})

    assert headers == {
        "Authorization": "Api-Key api-key",
        "X-Request-Id": "7928a3ec-05be-4819-9f80-a757c33293e9",
        "X-Request-Timeout": "42000",
        "X-Authorization": "Bearer auth_key",
    }


@patch("urllib.parse.urljoin")
def test_formation_url(mocked_urljoin):
    """
    Using the urllib.parse.urljoin method to form a URL.
    """

    yp_client = client.YandexPayClient("api-key", base_url="https://127.0.0.1/api/v1/")
    yp_client.get_url("test")

    mocked_urljoin.assert_called_once_with("https://127.0.0.1/api/v1/", "test")


@patch("requests.request", return_value=custom_response)
@patch("dd_yandex_pay.client.YandexPayClient.get_headers", return_value={})
def test_request_using_get_headers(mocked_get_headers, mocked_request):
    """
    Using the get_headers method on a request.
    """

    yp_client = client.YandexPayClient("api-key")
    yp_client.request("GET", "http://127.0.0.1/")
    mocked_get_headers.assert_called()
