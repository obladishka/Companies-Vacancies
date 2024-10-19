from typing import Any

import requests


def get_exchange_rates() -> dict[str, Any]:
    """Функция для получения актуального курса валют."""
    url = "https://www.cbr-xml-daily.ru/daily_json.js"

    response = requests.get(url)
    status_code = response.status_code

    if status_code == 200:
        return response.json()["Valute"]


def convert_to_ruble(currencies_rates: dict[str, Any], currency: str) -> float:
    """Функция для преобразования суммы в рубли."""
    value = currencies_rates.get(currency, {}).get("Value")
    nominal = currencies_rates.get(currency, {}).get("Nominal")
    if value and nominal:
        return round(value / nominal, 2)
    return 0
