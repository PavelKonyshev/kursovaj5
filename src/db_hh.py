import requests
from abc import ABC


class API(ABC):
    """
    Abstract class for API calls.
    """

    @staticmethod
    def get_company(self):
        pass


class HeadHunter(API):
    """
    Класс для подключения к API hh.ru и получения данных.
    """

    @staticmethod
    def get_company(company_list=[]) -> list:
        """
        Подключение к API 'https://api.hh.ru/employers'.
        Получение списка компаний с открытыми вакансиями ('only_with_vacancies': True).
        :param company_list: Cписок компаний.
        """
        url = 'https://api.hh.ru/employers'
        companies_list = []

        for company in company_list:
            response = requests.get(url, params={
                'text': company,
                'area': '113',
                'only_with_vacancies': True
            })

            if response.status_code != 200:
                print(f'Ошибка {response.status_code}')
            else:
                companies = response.json()['items']
                for el in companies:

                    companies_list.append(el)
        return companies_list

    @staticmethod
    def get_company_vacancies(companies_list=[]) -> list:
        """
        Получение списка открытых вакансий, найденных компаний с помощью ссылки (vacancies_url).
        :param companies_list: Список компаний.
        :return: Список открытых вакансий с обозначенной зарплатой ('only_with_salary': True), найденных компаний.
        """
        vacs_list = []
        for company in companies_list:
            vacancies_url = company['vacancies_url']
            response = requests.get(vacancies_url, params={'only_with_salary': True})
            if response.status_code != 200:
                print(f'Ошибка {response.status_code}')
            else:
                vacs = response.json()['items']
                for el in vacs:
                    vacs_list.append(el)
        return vacs_list