"""
Cases:

* Returning data.
* Using raise_for_status to raise errors.
* Raising errors.
* Returning an error if the status is not success.
* Raising an error if there is no data in the response.
* Successful check if data is available.
 """

from unittest.mock import patch

import pytest
import requests
from requests.exceptions import HTTPError

from dd_yandex_pay import YandexPayClient
from dd_yandex_pay.exceptions import YandexPayAPIError


def test_returning_data():
    """
    Returning data.
    """

    custom_response = requests.Response()
    custom_response.status_code = 200
    custom_response._content = b'{"status": "success"}'

    yp_client = YandexPayClient("api-key", base_url="http://127.0.0.1/")
    response = yp_client.response_handler(custom_response)

    assert response == {"status": "success"}


@patch("requests.models.Response.raise_for_status")
def test_using_raise_for_status(mocked_raise_for_status):
    """
    Using raise_for_status to return errors.
    """

    custom_response = requests.Response()
    custom_response.status_code = 200
    custom_response._content = b'{"status": "success"}'

    yp_client = YandexPayClient("api-key", base_url="http://127.0.0.1/")
    yp_client.response_handler(custom_response)

    mocked_raise_for_status.assert_called_once()


def test_raising_errors():
    """
    Raising errors.
    """

    custom_response = requests.Response()
    custom_response.status_code = 404
    custom_response.url = "http://127.0.0.1/404"
    custom_response.reason = "Not Found"

    yp_client = YandexPayClient("api-key", base_url="http://127.0.0.1/")

    msg = "404 Client Error: Not Found for url: http://127.0.0.1/404"
    with pytest.raises(HTTPError, match=msg):
        yp_client.response_handler(custom_response)


def test_raising_errors_with_fail_status():
    """
    Returning an error if the status is not success.
    """

    custom_response = requests.Response()
    custom_response.status_code = 200
    custom_response._content = b'{"status": "fail"}'

    yp_client = YandexPayClient("api-key", base_url="http://127.0.0.1/")

    msg = "Error unknown_error: Unknown error"
    with pytest.raises(YandexPayAPIError, match=msg) as exc_info:
        yp_client.response_handler(custom_response)

    assert exc_info.value.response == custom_response


def test_raising_error_with_no_data():
    """
    Raising an error if there is no data in the response.
    """

    custom_response = requests.Response()
    custom_response.status_code = 200
    custom_response._content = b'{"status": "success"}'

    yp_client = YandexPayClient("api-key", base_url="http://127.0.0.1/")

    msg = "Error has_no_data: Response has no data."
    with pytest.raises(YandexPayAPIError, match=msg) as exc_info:
        yp_client.response_handler(custom_response, True)

    assert exc_info.value.response == custom_response


def test_success_with_data():
    """
    Successful check if data is available.
    """

    custom_response = requests.Response()
    custom_response.status_code = 200
    custom_response._content = b'{"status": "success", "data": {}}'

    yp_client = YandexPayClient("api-key", base_url="http://127.0.0.1/")
    response = yp_client.response_handler(custom_response)

    assert response == {"status": "success", "data": {}}
