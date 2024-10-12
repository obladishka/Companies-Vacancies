from typing import Any

from src.hh_api import HHApi


class HHCompanies(HHApi):
    """Класс для работы с компаниями сайта hh.ru"""

    def __init__(self) -> None:
        """Метод для инициализации объектов класса."""
        super().__init__("https://api.hh.ru/employers")

    def __get_company(self, company_name: str) -> dict[str, Any]:
        """Приватный метод для получения информации о компании по названию."""
        response = super().get_response(text=company_name, sort_by="by_vacancies_open")
        companies = response.get("items")

        for company in companies:
            if len(company.get("name")) == len(company_name):
                return company
        return companies[0]

    def get_company(self, company_name: str) -> dict[str, Any]:
        """Публичный метод для получения информации о компании по названию и ее форматированию."""
        company = self.__get_company(company_name)
        return {"id": company.get("id"), "name": company.get("name"), "url": company.get("alternate_url")}
