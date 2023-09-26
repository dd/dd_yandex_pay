import uuid
from typing import Final
from typing import List
from typing import Optional
from typing import Union
from urllib.parse import urljoin

import requests


PRODUCTION_URL: Final[str] = "https://pay.yandex.ru/api/merchant/"
"""Боевой сервер"""

SANDBOX_URL: Final[str] = "https://sandbox.pay.yandex.ru/api/merchant/"
"""Тестовая среда"""


class YandexPayClient:
    """
    Клиент обёртка для [Yandex Pay API][yandex_pay_api_docs].

    [yandex_pay_api_docs]: https://pay.yandex.ru/ru/docs/custom/backend/yandex-pay-api/
    """

    RESOURCE_ORDER = "v1/orders"

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = PRODUCTION_URL,
        timeout: Optional[Union[float, int, tuple]] = (3, 10),
        deadline: Optional[int] = 10 * 1000,
    ):
        """
        Attributes:
            api_key: Ключи [Yandex Pay Merchant API][api_key].
            base_url: Базовый адрес Yandex Pay API.
            timeout: Дефолтный таймаут запроса для [requests][timeout].
            deadline: Дефолтный таймаут запроса в миллисекундах для [яндекс][deadline].

        [api_key]: https://console.pay.yandex.ru/web/account/settings/online
        [timeout]: https://requests.readthedocs.io/en/latest/user/advanced/#timeouts
        [deadline]: https://pay.yandex.ru/ru/docs/custom/backend/yandex-pay-api/
        """
        self.api_key = api_key
        self.base_url = base_url
        self.default_timeout = timeout
        self.default_deadline = deadline

    # Helpers

    def get_headers(self, custom: Optional[dict] = None) -> dict:
        """
        Создаёт заголовки для запроса.

        Attributes:
            custom: Объект с дополнительными заголовками (так же с помощью этого объекта можно
                переопределить генерируемые заголовки).

        Returns:
            Объект с заголовками.
        """

        return {
            "Authorization": f"Api-Key {self.api_key}",
            "X-Request-Id": str(uuid.uuid4()),
            "X-Request-Timeout": str(self.default_deadline),
            # "X-Request-Attempt": 1, ???
            **(custom or {}),
        }

    def get_url(self, resourse: str) -> str:
        """
        Формирует адрес для запроса к API.

        Attributes:
            resourse: Ресурс к которому необходимо выполнить запрос.

        Returns:
            Адрес для запроса.
        """

        return urljoin(self.base_url, resourse)

    def request(
        self,
        method: str,
        url: str,
        headers: Optional[dict] = None,
        raise_errors: Optional[bool] = True,
        **kwargs,
    ) -> requests.Response:
        """
        Метод для выполнения запросов к Yandex Pay API.

        Attributes:
            method: Метод запроса.
            url: Запрашиваемый ресурс.
            headers: Объект с заголовками.
            raise_errors: Объект с кастомными заголовками.
            kwargs: Объект с кастомными заголовками.

        Returns:
            Полученый ответ.
        """
        kwargs.setdefault("timeout", self.default_timeout)
        kwargs["headers"] = self.get_headers(headers)
        response = requests.request(method, url, **kwargs)

        if raise_errors:
            response.raise_for_status()

        return response

    # API

    def create_order(
        self,
        cart: dict,
        currencyCode: str,
        orderId: str,
        redirectUrls: dict,
        availablePaymentMethods: Optional[List[str]] = None,
        extensions: Optional[dict] = None,
        ttl: Optional[int] = None,
        raise_errors: Optional[int] = True,
        **kwargs: dict,
    ) -> requests.Response:
        """
        Запрос для создания ссылки на оплату.

        Подбронее о данных и ответе в документации [яндекса][docs].

        Attributes:
            cart: [Корзина][cart].
            currencyCode: Трехбуквенный код валюты заказа (ISO 4217).
            orderId: Идентификатор заказа.
            redirectUrls: [Ссылки для переадресации][redirect_urls] пользователя с формы оплаты.
            availablePaymentMethods: Доступные методы оплаты на платежной форме Яндекс Пэй.
            extensions: [Дополнительные параметры][extensions] для оформления оффлайн заказа.
            ttl: Время жизни заказа (в секундах).
            raise_errors: Флаг, вызывать ошибки с помощью метода
                [raise_for_status][requests.Response.raise_for_status] или нет.
            kwargs: Прочие дополнительные параметры метода [request][requests.request] кроме method,
                url и json.

        Returns:
            Полученый ответ API.

        [docs]: https://pay.yandex.ru/ru/docs/custom/backend/yandex-pay-api/order/merchant_v1_orders-post
        [cart]: https://pay.yandex.ru/ru/docs/custom/backend/yandex-pay-api/order/merchant_v1_orders-post#renderedcart
        [redirect_urls]: https://pay.yandex.ru/ru/docs/custom/backend/yandex-pay-api/order/merchant_v1_orders-post#merchantredirecturls
        [extensions]: https://pay.yandex.ru/ru/docs/custom/backend/yandex-pay-api/order/merchant_v1_orders-post#orderextensions
        """
        json = {
            # "availablePaymentMethods": availablePaymentMethods,
            "cart": cart,
            "currencyCode": currencyCode,
            # "extensions": extensions,
            "orderId": orderId,
            "redirectUrls": redirectUrls,
            # "ttl": ttl,
        }

        if availablePaymentMethods:
            json["availablePaymentMethods"] = availablePaymentMethods

        if extensions:
            json["extensions"] = extensions

        if ttl:
            json["ttl"] = ttl

        response = self.request("POST", self.get_url(self.RESOURCE_ORDER), json=json, **kwargs)

        return response
