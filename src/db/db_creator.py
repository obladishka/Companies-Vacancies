import psycopg2


class DBCreator:
    """Класс для создания базы данных."""

    def __init__(self, name: str, params: dict[str, str]) -> None:
        """Метод для инициализации объектов класса."""
        self.__name = name if name else "postgres"
        self.__params = params

    def create_database(self) -> None:
        """Метод для создания базы данных."""

        conn = psycopg2.connect(dbname="postgres", **self.__params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"DROP DATABASE IF EXISTS {self.__name}")
        cur.execute(f"CREATE DATABASE {self.__name}")

        cur.close()
        conn.close()

    def create_table_companies(self) -> None:
        """Метод для создания таблицы компаний."""
        conn = psycopg2.connect(dbname=self.__name, **self.__params)

        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE companies (
                    company_id VARCHAR,
                    company_name VARCHAR(255) NOT NULL,
                    company_url VARCHAR,
                    
                    CONSTRAINT pk_companies_company_id PRIMARY KEY (company_id)
                );
            """
            )

        conn.commit()
        conn.close()

    def create_table_vacancies(self) -> None:
        """Метод для создания таблицы вакансий."""
        conn = psycopg2.connect(dbname=self.__name, **self.__params)

        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE vacancies (
                    vacancy_id VARCHAR,
                    company_id VARCHAR,
                    vacancy_name VARCHAR(255) NOT NULL,
                    salary INT NOT NULL,
                    vacancy_url VARCHAR,

                    CONSTRAINT pk_vacancies_vacancy_id PRIMARY KEY (vacancy_id),
                    CONSTRAINT fk_vacancies_company_id FOREIGN KEY (company_id) REFERENCES companies(company_id)
                );
            """
            )

        conn.commit()
        conn.close()
