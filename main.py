from itertools import chain

from config.config import config
from src.db.db_manager import DBManager
from src.db.db_saver import DBSaver
from src.hh.hh_companies import HHCompanies
from src.hh.hh_vacancies import HHVacancies


def main():
    """Главная функция для использования приложения."""

    default_companies = ["Яндекс", "VK", "Т-банк", "Ozon", "Т1", "МТС", "Сбер", "Ланит", "Альфа-Банк", "Lamoda"]

    user_input = input(
        """Введите названия 10 компаний, от который Вы хотели бы получать вакансии, 
через запятую или пробел, или нажмите Enter, чтобы выбрать компании по умолчанию.
Компании по умолчанию: Яндекс, VK, Т-банк, Ozon, Т1, МТС, Сбер, Ланит, Альфа-Банк, Lamoda \n"""
    )

    print("Данные загружаются...")

    if user_input:
        default_companies = user_input.replace(",", " ").replace("  ", " ").split()

    hh = HHCompanies()
    companies = []
    for company in default_companies:

        if not hh.get_company(company):
            user_input = input(f"Компания {company} не найдена, введите другое название: ")
            default_companies.remove(company)
            default_companies.append(user_input)
            continue
        else:
            companies.append(hh.get_company(company))

    hh = HHVacancies()
    vacancies = list(chain(*[hh.get_vacancies(company.get("id")) for company in companies]))

    print("\nКомпании и вакансии успешно получены.")

    db_name = input(
        "Для загрузки данный введите название базы данных "
        "или нажмите Enter, чтобы выбрать название по умолчанию (postgres). "
    )
    params = config()

    db_saver = DBSaver(db_name, params)
    db_saver.create_database()

    db_saver.create_table_companies()
    db_saver.save_data_to_companies(companies)

    db_saver.create_table_vacancies()
    db_saver.save_data_to_vacancies(vacancies)

    print("\nДанные успешно сохранены.")

    while True:
        user_input = input(
            """\nВыберите интересующий Вас пункт меню:
    1. Получить список всех компаний с указанием количества вакансий у них
    2. Получить список всех найденных вакансий
    3. Вычислить среднюю зарплату по вакансиям
    4. Получить список всех вакансий, у которых зарплата выше средней
    5. Получить список вакансий, содержащих определенное слово в названии
    """
        )
        db_manager = DBManager(db_name, params)

        if user_input.strip() == "1":
            user_input = input("\nХотите отсортировать данные по количеству вакансий? да/нет ")
            if user_input.strip().lower() == "да":
                user_input = input("\nОтсортировать по убыванию? да/нет ")
                if user_input.strip().lower() == "да":
                    print(db_manager.get_companies_and_vacancies_count(is_order=True, is_descending=True))
                else:
                    print(db_manager.get_companies_and_vacancies_count(is_order=True, is_descending=False))
            else:
                print(db_manager.get_companies_and_vacancies_count(is_order=False, is_descending=False))

        elif user_input.strip() == "2":
            print(db_manager.get_all_vacancies())

        elif user_input.strip() == "3":
            print(db_manager.get_avg_salary())

        elif user_input.strip() == "4":
            avg_salary = db_manager.get_avg_salary()
            user_input = input("\nХотите отсортировать данные по зарплате? да/нет ")
            if user_input.strip().lower() == "да":
                user_input = input("\nОтсортировать по убыванию? да/нет ")
                if user_input.strip().lower() == "да":
                    print(db_manager.get_vacancies_with_higher_salary(avg_salary, is_order=True, is_descending=True))
                else:
                    print(db_manager.get_vacancies_with_higher_salary(avg_salary, is_order=True, is_descending=False))
            else:
                print(db_manager.get_vacancies_with_higher_salary(avg_salary, is_order=False, is_descending=False))

        elif user_input.strip() == "5":
            word = input("\nВведите слово для поиска: ")
            print(db_manager.get_vacancies_with_keyword(word))

        else:
            print("\n Я не знаю такой команды.")

        user_input = input("Хотите продолжить? да/нет ")
        if user_input.strip().lower() == "да":
            continue
        else:
            print("\nДо скорых встреч!")
            break


if __name__ == "__main__":
    main()
