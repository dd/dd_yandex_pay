# YandexPayClient

Для инициализации клиенту необходимо передать api-ключ:

```pycon
>>> from dd_yandex_pay import client
>>> yp_client = client.YandexPayClient("api-key"), base_url=client.SANDBOX_URL)
```

Так же в клиент можно передать несколько [дополнительных параметров][dd_yandex_pay.client.YandexPayClient].


## Creating order aka payment link

Для создания ссылки на оплату в наличии метод [create_order][dd_yandex_pay.client.YandexPayClient.create_order].

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
>>> response = yp_client.create_order(
...     cart=cart,
...     currencyCode="RUB",
...     orderId="test #1/1",
...     redirectUrls={
...         "onError": "https://127.0.0.1/error",
...         "onSuccess": "https://127.0.0.1/success",
...     },
... )
```

!!! info
	Обратите внимание что хоть в Yandex Pay API и подразумевается что протокол общения с API будет происходить не через http code 200, а статус обработки запроса будет отражаться в [теле ответа](https://pay.yandex.ru/ru/docs/custom/backend/yandex-pay-api/order/merchant_v1_orders-post#200-ok) (в котором есть поля _status_ и _code_), на деле в случае ошибки API вернёт ответ с http кодом соответствующей ошибки (например 401 в случае неправильного токена, или 400 в случае неверных данных в теле запроса).
