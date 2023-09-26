# Getting started


## Installation

Библиотека доступна для установки из [pypi](https://pypi.org/project/dd_yandex_pay/), поэтому установка максимально проста:

```console
$ pip install dd_yandex_pay
$ python
Python 3.11.4 (main, Jul 24 2023, 00:43:11) [GCC 11.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> dd_yandex_pay.__version__
'0.1.0'
```


## Let's start

Для взаимодействия с [Yandex Pay API][yandex_pay_api_docs] реализован интерфейс в виде класса [YandexPayClient][yandexpayclient] с набором методов для обращения к каждому из ендпоинтов API:

* [create_order][creating-order-aka-payment-link]


[yandex_pay_api_docs]: https://pay.yandex.ru/ru/docs/custom/backend/yandex-pay-api/
