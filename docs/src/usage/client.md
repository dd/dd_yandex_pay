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

Для создания ссылки на оплату есть метод [create_order][dd_yandex_pay.yp_client.YandexPayClient.create_order].

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

Получить данные заказа можно используя метод [get_order][dd_yandex_pay.yp_client.YandexPayClient.get_order]:

```pycon linenums="0"
>>> response_data = yp_client.get_order("test_1")
>>> print(response_data)
{
    "delivery": {},
    "operations": [],
    "order": {},
}
```
