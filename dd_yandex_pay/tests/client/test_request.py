"""
Cases:
  * Using the get_headers method on a request.
 """

from unittest.mock import patch

import requests

from dd_yandex_pay import YandexPayClient


custom_response = requests.Response()
custom_response.status_code = 200


@patch("requests.request", return_value=custom_response)
@patch("dd_yandex_pay.yp_client.YandexPayClient.get_headers", return_value={})
def test_request_using_get_headers(mocked_get_headers, mocked_request):
    """
    Using the get_headers method on a request.
    """

    yp_client = YandexPayClient("api-key")
    yp_client.request("GET", "http://127.0.0.1/")
    mocked_get_headers.assert_called()
