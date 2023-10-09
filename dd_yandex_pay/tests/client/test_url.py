"""
Cases:
  * Using the urllib.parse.urljoin method to form a URL.
 """

from unittest.mock import patch

from dd_yandex_pay import YandexPayClient


@patch("urllib.parse.urljoin")
def test_formation_url(mocked_urljoin):
    """
    Using the urllib.parse.urljoin method to form a URL.
    """

    yp_client = YandexPayClient("api-key", base_url="https://127.0.0.1/api/v1/")
    yp_client.get_url("test")

    mocked_urljoin.assert_called_once_with("https://127.0.0.1/api/v1/", "test")
