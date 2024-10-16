import pandas as pd
import psycopg2

from src.db.db_creator import DBCreator

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)


class DBManager(DBCreator):
    """Класс для работы с базой данных."""

    def __init__(self, name: str, params: dict[str, str]) -> None:
        """Метод для инициализации объектов класса."""
        super().__init__(name, params)

    def get_companies_and_vacancies_count(self, is_order: bool = False, is_descending: bool = False):
        """Метод для получения количества вакансий у каждой компании."""
        basic_query = """
            SELECT company_name, COUNT (vacancy_name) as vacancies_total
            FROM companies
            LEFT JOIN vacancies USING(company_id)
            GROUP BY company_name
        """
        order_query = "" if not is_order else "\nORDER BY vacancies_total"
        descending_query = "" if not is_descending else " DESC"
        query = basic_query + order_query + descending_query

        conn = psycopg2.connect(dbname=self._name, **self._params)

        with conn.cursor() as cur:
            cur.execute(query)
            names = [x[0] for x in cur.description]
            rows = cur.fetchall()
            result = pd.DataFrame(rows, columns=names)

        conn.close()
        return result

    def get_all_vacancies(self):
        """Метод для получения списка всех вакансий."""
        conn = psycopg2.connect(dbname=self._name, **self._params)

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT company_name, vacancy_name, salary, vacancy_url
                FROM companies
                LEFT JOIN vacancies USING(company_id)
                """
            )
            names = [x[0] for x in cur.description]
            rows = cur.fetchall()
            result = pd.DataFrame(rows, columns=names)

        conn.close()
        return result

    def get_avg_salary(self):
        """Метод для получения средней зарплаты по вакансиям."""
        conn = psycopg2.connect(dbname=self._name, **self._params)

        with conn.cursor() as cur:
            cur.execute("SELECT AVG(salary) FROM vacancies")
            names = [x[0] for x in cur.description]
            rows = cur.fetchall()
            result = pd.DataFrame(rows, columns=names)

        conn.close()
        return round(result["avg"][0], 2)

    def get_vacancies_with_higher_salary(self, avg_salary: float, is_order: bool = False, is_descending: bool = False):
        """Метод для получения списка всех вакансий, у которых зарплата выше средней."""
        basic_query = f"SELECT * FROM vacancies WHERE salary > {avg_salary}"
        order_query = "" if not is_order else "\nORDER BY salary"
        descending_query = "" if not is_descending else " DESC"
        query = basic_query + order_query + descending_query

        conn = psycopg2.connect(dbname=self._name, **self._params)

        with conn.cursor() as cur:
            cur.execute(query)
            names = [x[0] for x in cur.description]
            rows = cur.fetchall()
            result = pd.DataFrame(rows, columns=names)

        conn.close()
        return result

    def get_vacancies_with_keyword(self, key_word: str):
        """Метод для получения списка всех вакансий, в названии которых содержится переданное в метод слово."""
        conn = psycopg2.connect(dbname=self._name, **self._params)

        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM vacancies WHERE vacancy_name LIKE '%{key_word[:-3]}%'")
            names = [x[0] for x in cur.description]
            rows = cur.fetchall()
            result = pd.DataFrame(rows, columns=names)

        conn.close()
        return result
