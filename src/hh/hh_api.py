from typing import Any

import requests


class HHApi:
    """Родительский класс для работы с платформой hh.ru"""

    url: str
    headers: dict
    params: dict

    def __init__(self, url: str) -> None:
        """Метод для инициализации объектов класса."""
        self.__url = url
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {}

    def __get_response(self, params: dict[str, Any]) -> None | dict[str, Any]:
        """Закрытый метод для подключения к API сайта hh.ru."""

        try:
            self.response = requests.get(self.__url, headers=self.__headers, params=params)
        except requests.exceptions.RequestException as ex:
            print(ex)
        else:
            if self.response.status_code == 200:
                return self.response.json()

    def _get_response(self, **kwargs) -> None | dict:
        """Публичный метод для подключения к API сайта hh.ru."""
        self.__params = dict(**kwargs)
        return self.__get_response(self.__params)
