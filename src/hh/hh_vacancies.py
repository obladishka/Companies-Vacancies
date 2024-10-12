from typing import Any

from src.hh.hh_api import HHApi


class HHVacancies(HHApi):
    """Класс для получения информации о вакансиях компаний с сайта hh.ru."""

    def __init__(self) -> None:
        """Метод для инициализации объектов класса."""
        super().__init__("https://api.hh.ru/vacancies")

    def __get_vacancies(self, company_id: str) -> list[dict[str, Any]]:
        """Приватный метод для получения вакансий определенной компании."""
        vacancies = []
        page = 0

        while page < 20:
            response = super()._get_response(page=page, per_page=100, employer_id=company_id)
            if not response:
                break
            if response:
                vacancies.extend(response.get("items"))
            page += 1

        return vacancies

    def get_vacancies(self, company_id: str) -> list[dict[str, Any]]:
        """Публичный метод для получения вакансий определенной компании и их форматированию."""
        vacancies = self.__get_vacancies(company_id)
        result = []
        for vacancy in vacancies:
            vacancy_dict = {
                "id": vacancy.get("id"),
                "company": vacancy.get("employer").get("name"),
                "name": vacancy.get("name"),
                "salary": (
                    vacancy.get("salary").get("to")
                    if vacancy.get("salary") and vacancy.get("salary").get("to")
                    else (
                        vacancy.get("salary").get("from") * 1.5
                        if vacancy.get("salary") and vacancy.get("salary").get("from")
                        else None
                    )
                ),
                "currency": (
                    vacancy.get("salary").get("currency")
                    if vacancy.get("salary")
                    else "BYN" if vacancy.get("salary") and vacancy.get("salary").get("currency") == "BYR" else "RUR"
                ),
                "url": vacancy.get("alternate_url"),
            }
            result.append(vacancy_dict)
        return result
