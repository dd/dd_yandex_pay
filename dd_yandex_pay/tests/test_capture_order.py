"""
Cases:
  * Checking the sent data.
  * Request with a full set of request parameters.
  * Using the get_url method.
  * Checking the use of the YandexPayClient.request method.
  * Passing additional parameters to requests.request.
  * Checking the use of the YandexPayClient.response_handler method.
  * Checking the returned data using the method.
  * Checking character conversion in paths.
"""

import json
from unittest.mock import patch

import requests

from dd_yandex_pay import YandexPayClient


response_data = {
    "code": 200,
    "status": "success",
    "data": {
        "amount": 123.45,
        "operationId": "1c4a7fc7-219f-493f-996a-02c9ef549bf9",
        "operationType": "AUTHORIZE",
        "orderId": "123456",
    },
}

custom_response = requests.Response()
custom_response.status_code = 200
custom_response._content = bytes(json.dumps(response_data), "utf-8")


@patch("requests.request", return_value=custom_response)
@patch("uuid.uuid4", return_value="913a1867-aeb8-4ca8-9c83-b2ad4c2c6f4a")
def test_request_data(mocked_uuid4, mocked_request):
    """
    Checking the sent data.
    """

    yp_client = YandexPayClient("api-key", base_url="http://127.0.0.1/")
    yp_client.capture_order(order_id="test_123456")

    mocked_request.assert_called_once_with(
        "POST",
        "http://127.0.0.1/v1/orders/test_123456/capture",
        json={},
        timeout=(3, 10),
        headers={
            "Authorization": "Api-Key api-key",
            "X-Request-Id": "913a1867-aeb8-4ca8-9c83-b2ad4c2c6f4a",
            "X-Request-Timeout": "10000",
        },
    )


@patch("requests.request", return_value=custom_response)
def test_all_data_params(mocked_request):
    """
    Request with a full set of request parameters.
    """

    yp_client = YandexPayClient("api-key", base_url="http://127.0.0.1/")
    yp_client.capture_order(
        order_id="test_123456",
        cart={"cartId": "123456"},
        externalOperationId="123456",
        orderAmount=123.45,
        shipping={"amount": 123.45, "methodType": "DIRECT"},
    )

    mocked_request.assert_called_once()
    assert mocked_request.call_args.kwargs["json"] == {
        "cart": {"cartId": "123456"},
        "externalOperationId": "123456",
        "orderAmount": 123.45,
        "shipping": {"amount": 123.45, "methodType": "DIRECT"},
    }


@patch("dd_yandex_pay.yp_client.YandexPayClient.get_url", return_value="http://127.0.0.1/")
@patch("requests.request", return_value=custom_response)
def test_usage_yandexpayclient_get_url(mocked_request, mocked_get_url):
    """
    Using the get_url method.
    """

    yp_client = YandexPayClient("api-key", base_url="http://127.0.0.1/")
    yp_client.capture_order(order_id="test_123456")

    mocked_get_url.assert_called_once_with("v1/orders/test_123456/capture")


@patch("dd_yandex_pay.yp_client.YandexPayClient.request", return_value=custom_response)
def test_usage_request(mocked_request):
    """
    Checking the use of the YandexPayClient.request method.
    """

    yp_client = YandexPayClient("api-key", base_url="http://127.0.0.1/")
    yp_client.capture_order(order_id="test_123456")

    mocked_request.assert_called_once()


@patch("uuid.uuid4", return_value="7928a3ec-05be-4819-9f80-a757c33293e9")
@patch("requests.request", return_value=custom_response)
def test_passing_additional_parameters(mocked_request, mocked_uuid4):
    """
    Passing additional parameters to requests.request.
    """

    yp_client = YandexPayClient("api-key", base_url="http://127.0.0.1/")
    yp_client.capture_order(
        order_id="test_123456",
        allow_redirects=False,
        cookies={"foo": "bar"},
        headers={"X-Authorization": "Bearer auth_key"},
    )

    mocked_request.assert_called_once()
    assert mocked_request.call_args.kwargs["allow_redirects"] is False
    assert mocked_request.call_args.kwargs["cookies"] == {"foo": "bar"}
    assert mocked_request.call_args.kwargs["headers"] == {
        "Authorization": "Api-Key api-key",
        "X-Request-Id": "7928a3ec-05be-4819-9f80-a757c33293e9",
        "X-Request-Timeout": "10000",
        "X-Authorization": "Bearer auth_key",
    }


@patch("dd_yandex_pay.yp_client.YandexPayClient.response_handler")
@patch("requests.request", return_value=custom_response)
def test_usage_response_handler(mocked_request, mocked_handler):
    """
    Checking the use of the YandexPayClient.response_handler method.
    """

    yp_client = YandexPayClient("api-key", base_url="http://127.0.0.1/")
    yp_client.capture_order(order_id="test_123456")

    mocked_handler.assert_called_once_with(custom_response, True)


@patch("requests.request", return_value=custom_response)
def test_returned_data(mocked_request):
    """
    Checking the returned data using the method.
    """

    yp_client = YandexPayClient("api-key", base_url="http://127.0.0.1/")
    response = yp_client.capture_order(order_id="test_123456")

    assert response == response_data["data"]


@patch("requests.request", return_value=custom_response)
def test_character_conversion(mocked_request):
    """
    Checking character conversion in paths.
    """

    yp_client = YandexPayClient("api-key", base_url="http://127.0.0.1/")
    yp_client.capture_order(order_id="test #1/1")

    assert mocked_request.call_args.args[1] == "http://127.0.0.1/v1/orders/test%20%231%2F1/capture"
