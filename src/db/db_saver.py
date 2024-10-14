from typing import Any

import psycopg2

from src.db.db_creator import DBCreator


class DBSaver(DBCreator):
    """Класс для заполнения базы данных."""

    def __init__(self, name: str, params: dict[str, str]) -> None:
        """Метод для инициализации объектов класса."""
        super().__init__(name, params)

    def save_data_to_companies(self, companies: list[dict[str, Any]]) -> None:
        """Метод для заполнения таблицы компаний."""
        conn = psycopg2.connect(dbname=self.__name, **self.__params)

        with conn.cursor() as cur:
            for company in companies:
                cur.execute(
                    """
                    INSERT INTO companies (company_id, company_name, company_url)
                    VALUES (%s, %s, %s)
                    """,
                    (company.get("id"), company.get("name"), company.get("url"))
                )

        conn.commit()
        conn.close()

    def save_data_to_vacancies(self, vacancies: list[dict[str, Any]]) -> None:
        """Метод для заполнения таблицы вакансий."""
        conn = psycopg2.connect(dbname=self.__name, **self.__params)

        with conn.cursor() as cur:
            for vacancy in vacancies:
                cur.execute(
                    """
                    INSERT INTO vacancies (vacancy_id, company_id, vacancy_name, salary, vacancy_url)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        vacancy.get("id"),
                        vacancy.get("company_id"),
                        vacancy.get("name"),
                        vacancy.get("salary"),
                        vacancy.get("url"))
                    )

        conn.commit()
        conn.close()
