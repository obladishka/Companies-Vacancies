from typing import Any

from src.hh.hh_api import HHApi
from src.utils import convert_to_ruble, get_exchange_rates


class HHVacancies(HHApi):
    """Класс для получения информации о вакансиях компаний с сайта hh.ru."""

    def __init__(self) -> None:
        """Метод для инициализации объектов класса."""
        super().__init__("https://api.hh.ru/vacancies")

    def __get_vacancies(self, company_id: str) -> list[dict[str, Any]]:
        """Приватный метод для получения вакансий определенной компании."""
        vacancies = []

        response = super()._get_response(per_page=100, employer_id=company_id)
        vacancies.extend(response.get("items"))

        return vacancies

    def get_vacancies(self, company_id: str) -> list[dict[str, Any]]:
        """Публичный метод для получения вакансий определенной компании и их форматированию."""
        vacancies = self.__get_vacancies(company_id)
        exchange_rates = get_exchange_rates()
        result = []

        for vacancy in vacancies:
            raw_salary = (
                vacancy.get("salary").get("to")
                if vacancy.get("salary") and vacancy.get("salary").get("to")
                else (
                    vacancy.get("salary").get("from") * 1.5
                    if vacancy.get("salary") and vacancy.get("salary").get("from")
                    else 0
                )
            )
            currency = (
                vacancy.get("salary").get("currency")
                if vacancy.get("salary")
                else "BYN" if vacancy.get("salary") and vacancy.get("salary").get("currency") == "BYR" else "RUR"
            )

            vacancy_dict = {
                "company_id": company_id,
                "name": vacancy.get("name"),
                "salary": raw_salary if currency == "RUR" else raw_salary * convert_to_ruble(exchange_rates, currency),
                "url": vacancy.get("alternate_url"),
            }
            result.append(vacancy_dict)
        return result
