"""
Cases:
  * Checking the sent data.
  * Request with a full set of request parameters.
  * Using the get_url method.
  * Checking the use of the YandexPayClient.request method.
  * Passing additional parameters to requests.request.
  * Checking the use of the YandexPayClient.response_handler method.
  * Checking the returned data using the method.
"""

import json
from unittest.mock import patch

import requests

from dd_yandex_pay import YandexPayClient
from dd_yandex_pay import constants


cart = {
    "externalId": "test_1",
    "items": [
        {
            "productId": "test",
            "quantity": {
                "count": "2",
                "label": "шт",
            },
            "title": "Тестовый товар",
            "unitPrice": "100.00",
            "subtotal": "200.00",
            "discountedUnitPrice": "90.00",
            "total": "180.00",
        }
    ],
    "total": {
        "amount": "180.00",
    },
}

data = {
    "cart": cart,
    "currencyCode": "RUB",
    "orderId": "test #1/1",
    "redirectUrls": {
        "onError": "http://127.0.0.1/error",
        "onSuccess": "http://127.0.0.1/success",
    },
}

response_data = {
    "code": 200,
    "status": "success",
    "data": {"paymentUrl": "http://127.0.0.1/payment_url"},
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
    yp_client.create_order(
        cart=cart,
        currencyCode=data["currencyCode"],
        orderId=data["orderId"],
        redirectUrls=data["redirectUrls"],
    )

    mocked_request.assert_called_once_with(
        "POST",
        "http://127.0.0.1/v1/orders",
        json=data,
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
    yp_client.create_order(
        cart=cart,
        currencyCode=data["currencyCode"],
        orderId=data["orderId"],
        redirectUrls=data["redirectUrls"],
        availablePaymentMethods=[constants.PAYMENT_METHODS_CARD],
        extensions={"qrData": {"token": "qr_token"}},
        ttl=60000,
    )

    mocked_request.assert_called_once()
    assert mocked_request.call_args.kwargs["json"] == {
        **data,
        "availablePaymentMethods": ["CARD"],
        "extensions": {"qrData": {"token": "qr_token"}},
        "ttl": 60000,
    }


@patch("dd_yandex_pay.yp_client.YandexPayClient.get_url", return_value="http://127.0.0.1/")
@patch("requests.request", return_value=custom_response)
def test_usage_yandexpayclient_get_url(mocked_request, mocked_get_url):
    """
    Using the get_url method.
    """

    yp_client = YandexPayClient("api-key", base_url="http://127.0.0.1/")
    yp_client.create_order(
        cart=cart,
        currencyCode=data["currencyCode"],
        orderId=data["orderId"],
        redirectUrls=data["redirectUrls"],
    )

    mocked_get_url.assert_called_once_with("v1/orders")


@patch("dd_yandex_pay.yp_client.YandexPayClient.request", return_value=custom_response)
def test_usage_request(mocked_request):
    """
    Checking the use of the YandexPayClient.request method.
    """

    yp_client = YandexPayClient("api-key", base_url="http://127.0.0.1/")
    yp_client.create_order(
        cart=cart,
        currencyCode=data["currencyCode"],
        orderId=data["orderId"],
        redirectUrls=data["redirectUrls"],
    )

    mocked_request.assert_called_once()


@patch("uuid.uuid4", return_value="7928a3ec-05be-4819-9f80-a757c33293e9")
@patch("requests.request", return_value=custom_response)
def test_passing_additional_parameters(mocked_request, mocked_uuid4):
    """
    Passing additional parameters to requests.request.
    """

    yp_client = YandexPayClient("api-key", base_url="http://127.0.0.1/")
    yp_client.create_order(
        cart=cart,
        currencyCode=data["currencyCode"],
        orderId=data["orderId"],
        redirectUrls=data["redirectUrls"],
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
    yp_client.create_order(
        cart=cart,
        currencyCode=data["currencyCode"],
        orderId=data["orderId"],
        redirectUrls=data["redirectUrls"],
    )

    mocked_handler.assert_called_once_with(custom_response, True)


@patch("requests.request", return_value=custom_response)
def test_returned_data(mocked_request):
    """
    Checking the returned data using the method.
    """

    yp_client = YandexPayClient("api-key", base_url="http://127.0.0.1/")
    response = yp_client.create_order(
        cart=cart,
        currencyCode=data["currencyCode"],
        orderId=data["orderId"],
        redirectUrls=data["redirectUrls"],
    )

    assert response == response_data["data"]
