"""
Cases:
  * Checking default headers.
  * Checking header overrides.
  * Checking custom headers.
 """

from unittest.mock import patch

from dd_yandex_pay import YandexPayClient


@patch("uuid.uuid4", return_value="7928a3ec-05be-4819-9f80-a757c33293e9")
def test_default_headers(mocked_uuid4):
    """
    Checking default headers.
    """

    yp_client = YandexPayClient("api-key", deadline=42000)
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

    yp_client = YandexPayClient("api-key", deadline=42000)
    headers = yp_client.get_headers(**overided_headers)
    assert headers == overided_headers


@patch("uuid.uuid4", return_value="7928a3ec-05be-4819-9f80-a757c33293e9")
def test_custom_headers(mocked_uuid4):
    """
    Checking custom headers.
    """

    yp_client = YandexPayClient("api-key", deadline=42000)
    headers = yp_client.get_headers(**{"X-Authorization": "Bearer auth_key"})

    assert headers == {
        "Authorization": "Api-Key api-key",
        "X-Request-Id": "7928a3ec-05be-4819-9f80-a757c33293e9",
        "X-Request-Timeout": "42000",
        "X-Authorization": "Bearer auth_key",
    }
