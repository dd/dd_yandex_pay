# YandexPayClient

Минимально для инициализации клиенту необходимо передать api-ключ:

```pycon linenums="0"
>>> from dd_yandex_pay import YandexPayClient
>>> yp_client = YandexPayClient("api-key", base_url="https://sandbox.pay.yandex.ru/api/merchant/")
```

Базовый урл не обязательный параметр и по умолчанию настроен на боевое API.

Так же в клиент можно передать несколько [дополнительных параметров][dd_yandex_pay.yp_client.YandexPayClient].

!!! note
	Так же следует отметить что все методы клиента возвращают не весь контент ответа, а только лишь объект `data` из ответа. Так как остальная часть тела ответа отражает статус запроса, и в случае успешного запроса всегда равна одним и тем же данным, эти данные было решено игнорировать. В случае каких либо ошибок, запрос можно найти в полу `response` в ошибке.


## Creating order aka payment link

Для [API создания ссылки](https://pay.yandex.ru/ru/docs/custom/backend/yandex-pay-api/order/merchant_v1_orders-post) на оплату есть метод [create_order][dd_yandex_pay.yp_client.YandexPayClient.create_order].

```pycon linenums="0"
>>> cart = {
...     "externalId": "test_1",
...     "items": [
...         {
...             "productId": "test",
...             "quantity": {
...                 "count": "2",
...                 "label": "шт",
...             },
...             "title": "Тестовый товар",
...             "unitPrice": "100.00",
...             "subtotal": "200.00",
...             "discountedUnitPrice": "90.00",
...             "total": "180.00",
...         }
...     ],
...     "total": {
...         "amount": "180.00",
...     },
... }
>>> response_data = yp_client.create_order(
...     cart=cart,
...     currencyCode="RUB",
...     orderId="test #1/1",
...     redirectUrls={
...         "onError": "https://127.0.0.1/error",
...         "onSuccess": "https://127.0.0.1/success",
...     },
... )
>>> print(response_data)
{'paymentUrl': 'https://sandbox.pay.ya.ru/a/bcdefg'}
```

!!! info
	Обратите внимание, читая [документацию](https://pay.yandex.ru/ru/docs/custom/backend/yandex-pay-api/order/merchant_v1_orders-post#200-ok) Yandex Pay API может показаться что статус запроса будет отдаваться в теле ответа в параметрах _status_ и _code_, а http код всегда 200 и будет отражать сетевое состояние, но на деле, это не так, если например выполнить запрос с заведомо неверным ключом, вернётся 401 ошибка, а в теле ответа будет примерно такое содержимое:

	```json linenums="0"
	{
		"status": "fail",
		"reasonCode": "AUTHENTICATION_ERROR",
		"reason": "Malformed API key"
	}
	```

	а если выполнить запрос на создание ссылки на оплату с неверными данными, получим ответ с кодом 400 и следующим содержимым в теле ответа:

	```json linenums="0"
	{
		"status": "fail",
		"reasonCode": "ORDER_AMOUNT_MISMATCH",
		"reason": "Cart total amount mismatch: expected `cart_total` = `items_sum` - `discounts_sum`, but found 0.00 != 180.00 - 0.00",
		"details": {
			"cart_total": "0.00",
			"items_sum": "180.00",
			"discounts_sum": "0.00",
			"description": "Cart total amount mismatch: expected `cart_total` = `items_sum` - `discounts_sum`, but found 0.00 != 180.00 - 0.00"
		}
	}
	```


## Receving order details

Получить данные заказа можно отправив GET запрос на соответствующее [API](https://pay.yandex.ru/ru/docs/custom/backend/yandex-pay-api/order/merchant_v1_order-get) используя метод [get_order][dd_yandex_pay.yp_client.YandexPayClient.get_order]:

```pycon linenums="0"
>>> response_data = yp_client.get_order("test_1")
>>> print(response_data)
{
    "delivery": {},
    "operations": [],
    "order": {},
}
```


## Refund on order

Для возврата средств в API Yandex Pay есть два ендпоинта - [v1](https://pay.yandex.ru/ru/docs/custom/backend/yandex-pay-api/order/merchant_v1_refund-post) и [v2](https://pay.yandex.ru/ru/docs/custom/backend/yandex-pay-api/order/merchant_v2_refund-post), для этих ендпоинтов реализовано 2 метода [refund_order_v1][dd_yandex_pay.yp_client.YandexPayClient.refund_order_v1] и [refund_order_v2][dd_yandex_pay.yp_client.YandexPayClient.refund_order_v2] соответственно:


```pycon linenums="0"
>>> yp_client.refund_order_v1(
>>>     "test_1",
>>>     123.45,
>>>     123.45,
>>> )
{
    "operation": {
        # ...
    },
}
>>> yp_client.refund_order_v2(
>>>     "test_1",
>>>     123.45,
>>> )
{
    "operation": {
        # ...
    },
}
```


## Cancel order

Заказы в статусе `AUTHORIZED` можно [отменить](https://pay.yandex.ru/ru/docs/custom/backend/yandex-pay-api/order/merchant_v1_cancel-post) используя метод [cancel_order][dd_yandex_pay.yp_client.YandexPayClient.cancel_order]:

```pycon linenums="0"
>>> response_data = yp_client.cancel_order("test_1", "Canceling a test order.")
>>> print(response_data)
{
    "operation": {
        # ...
    },
}
```

!!! note
	Важно отметить, что это не отмена заказа, то есть с помощью этого метода не получится закрыть ссылку на оплату, что бы пользователь не смог ею воспользоваться. Это отмена списания заблокированных средств, а для списания средств используется метод [capture_order][dd_yandex_pay.yp_client.YandexPayClient.capture_order].


## Сapture order

Для [списания средств](https://pay.yandex.ru/ru/docs/custom/backend/yandex-pay-api/order/merchant_v1_capture-post) по заказам в статусе `AUTHORIZED` реализован метод [capture_order][dd_yandex_pay.yp_client.YandexPayClient.capture_order]:

```pycon linenums="0"
>>> response_data = yp_client.capture_order("test_1")
>>> print(response_data)
{
    "operation": {
        # ...
    },
}
```


## Receiving transaction data

Что бы получить [данные по операциям](https://pay.yandex.ru/ru/docs/custom/backend/yandex-pay-api/operation/merchant_v1_operations-get) воспользуйтесь методом [get_operation][dd_yandex_pay.yp_client.YandexPayClient.get_operation]:

```pycon linenums="0"
>>> response_data = yp_client.get_operation("test_1")
>>> print(response_data)
{
    "operation": {
        # ...
    },
}
```
