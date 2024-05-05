from config import config
from src.db_hh import HeadHunter
from src.func import (proc_company_data,
                      proc_vacs_data,
                      create_database,
                      save_data_employers_to_database,
                      save_data_vacancies_to_database)
from src.class_manager import DBManager


def main():

    # создаем экземпляр класса для подключения к API hh.ru
    hh = HeadHunter()

    # создаем список искомых компаний
    company_list = ['ВТБ',
                    'Ozon',
                    'Яндекс',
                    'Роснефть',
                    'СБЕР',
                    'Пятерочка',
                    'Аптеки ВИТА',
                    'Wildberries',
                    'Тинькофф',
                    'Норникель',
                    'МТС']

    print("Поиск вакансий в следующих компаниях:\n")
    print(', \n'.join(company_list))

    print("Добавить компании для поиска?(y/n)\n")
    user_answer = input()

    if user_answer in ['y', 'н']:
        print("Введите названия компаний через пробел\n")
        company_name = input('').split(' ')
        for company in company_name:
            company_list.append(company)

    print(', \n'.join(company_list))
    print("Идет загрузка данных...")

    # загружаем информацию о компаниях
    employers = hh.get_company(company_list)

    # загружаем информацию о вакансиях найденных компаний
    vacs = hh.get_company_vacancies(employers)

    # преобразуем полученные данные для сохранения в бд
    companies = proc_company_data(employers)
    vacancies = proc_vacs_data(vacs)

    # создаем базу данных 'hh_vacancies' и таблицы для сохранения данных о компаниях их вакансиях
    params = config()
    database_name = 'hh_vacancies'
    create_database(database_name, params)

    # сохраняем данные о компаниях и их вакансиях в бд 'hh_vacancies'
    save_data_employers_to_database(companies, database_name, params)
    save_data_vacancies_to_database(vacancies, database_name, params)

    # создаем экземпляр класса DBManager для вывода запросов
    db_manager = DBManager()

    # функционал взаимодействия с пользователем
    print('Все данные сохранены в базу данных hh_vacancies!')
    total_vacancies = db_manager.get_total_vacancies('hh_vacancies')
    print(f'Всего вакансий: {total_vacancies[0]}')
    print('Вывести информацию о найденных компаний?(y/n)')
    user_answer = input()
    if user_answer in ['y', 'н']:
        companies = db_manager.get_company_info('hh_vacancies')
        for company in companies:
            print(f"{company[0]}\n"
                  f"Ссылка {company[1]}\n"
                  f"Открытых вакансий: {company[2]}\n")

    print("Вывести на экран найденные вакансии?(y/n)")
    user_answer = input()
    if user_answer in ['y', 'н']:
        vacancies = db_manager.get_all_vacancies('hh_vacancies')
        for vacancy in vacancies:
            print(f"Название вакансии: {vacancy[1]}\n"
                  f"Город: {vacancy[2]}\n"
                  f"Описание: {vacancy[3]}\n"
                  f"Ссылка: {vacancy[4]}\n"
                  f"Оплата: {vacancy[5]}\n"
                  f"Требования: {vacancy[6]}\n"
                  f"Организация: {vacancy[8]}\n")

    print("Вывести на экран среднюю зарплату по найденным вакансиям?(y/n)")
    user_answer = input()
    if user_answer in ['y', 'н']:
        vacancies = db_manager.get_avg_salary('hh_vacancies')
        print(f"Средняя зарплата {vacancies[0]} ₽")

    print("Вывести на экран вакансии с зарплатой выше среднего?(y/n)")
    user_answer = input()
    if user_answer in ['y', 'н']:
        vacancies = db_manager.get_vacancies_with_higher_salary('hh_vacancies')
        for vacancy in vacancies:
            print(f"Название вакансии: {vacancy[0]}\n"
                  f"Город: {vacancy[3]}\n"
                  f"Ссылка: {vacancy[1]}\n"
                  f"Оплата: {vacancy[2]}\n"
                  f"Организация: {vacancy[4]}\n")

    print("Найти вакансии по ключевому слову?(y/n)")
    user_answer = input()
    if user_answer in ['y', 'н']:
        user_answer = input("Введите ключевое слово для поиска:\n").capitalize()
        vacancies = db_manager.get_vacancies_with_keyword('hh_vacancies', user_answer)
        for vacancy in vacancies:
            print(f"Название вакансии: {vacancy[0]}\n"
                  f"Город: {vacancy[3]}\n"
                  f"Ссылка: {vacancy[1]}\n"
                  f"Оплата: {vacancy[2]}\n"
                  f"Организация: {vacancy[4]}\n")

    print("Выход из программы?(y/n)")
    user_answer = input()
    if user_answer in ['y', 'н']:
        print('Все данные сохранены в базу данных hh_vacancies!')
        print('Выход из программы!')
    else:
        main()


if __name__ == '__main__':
    main()