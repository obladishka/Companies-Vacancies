# Вакансии компаний

Приложение, для поиска и загрузки вакансий только тех компаний, которые интересны именно Вам. Выберите понравившиеся 
компании и не тратьте время на бесконечное пролистывание неинтересных предложений.

## Начало работы

Для запуска приложения:

1. Клонируйте репозиторий, выполнив в своем терминале команду
```commandline
git clone https://github.com/obladishka/VacanciesProcessor.git
```
2. Установите зависимости через poetry:
```commandline
poetry intall
```
3. Переименуйте файл *database.ini.example* в *database.ini* и заполните его своими данными, для подключения к базе данных.
4. Запустите приложение, выполнив в терминале команду
```commandline
python3 main.py # для MacOC
python main.py # для Windows
```
5. Перед началом использования введите названия интересующих Вас компаний.

## Использование
Приложение предоставляет несколько удобных функций для быстрой фильтрации и анализа полученных вакансий:

*1. Получение списка всех компаний с указанием количества вакансий у них*

*2. Получение списка всех найденных вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию.*

*3. Вычисление средней зарплаты по вакансиям*

*4. Получение списка всех вакансий, у которых зарплата выше средней*

*5. Получение списка вакансий, содержащих определенное слово в названии*

## Источники
<a href="https://www.cbr-xml-daily.ru/">Курсы ЦБ РФ в XML и JSON, API</a>