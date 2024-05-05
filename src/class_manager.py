import psycopg2
from config import config


class DBManager:
    """
    Класс для запросов с базы данных 'hh_vacancies'.
    """

    def __init__(self):
        self.database = 'hh_vacancies'
        self.params = config()

    def get_company_info(self, database):
        """
        Получение информации о компании.
        """
        with psycopg2.connect(dbname=database, **self.params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT employers_name, employers_url, open_vacancies
                FROM employers;
                """)
                query = cur.fetchall()
        conn.close()
        return query

    def get_total_vacancies(self, database):
        """
        Количество найденных вакансий
        """
        with psycopg2.connect(dbname=database, **self.params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT COUNT(*)
                FROM vacancies;
                """)
                query = cur.fetchone()
        conn.close()
        return query

    def get_all_vacancies(self, database):
        """
        Получение N количества вакансий из найденных
        """
        with psycopg2.connect(dbname=database, **self.params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT *
                FROM vacancies;
                """)
                query = cur.fetchall()
        conn.close()
        return query

    def get_avg_salary(self, database):
        """
        Получение средней зарплаты вакансий.
        """
        with psycopg2.connect(dbname=database, **self.params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT ROUND(AVG(salary)::numeric, 2)
                FROM vacancies;
                """)
                query = cur.fetchone()
        conn.close()
        return query

    def get_vacancies_with_higher_salary(self, database):
        """
        Получение вакансий с зарплатой выше среднего по найденным.
        """
        with psycopg2.connect(dbname=database, **self.params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT vacancy_name, url, salary, city, employers_name
                FROM vacancies
                WHERE salary > (SELECT AVG(salary) from vacancies)
                """)
                query = cur.fetchall()
        conn.close()
        return query

    def get_vacancies_with_keyword(self, database, user_query):
        """
        Получает список всех вакансий,
        в названии которых содержится переданное в метод ключ слово.
        """
        with psycopg2.connect(dbname=database, **self.params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT vacancy_name, url, salary, city, employers_name
                FROM vacancies
                WHERE vacancy_name LIKE '%{}%'
                """.format(user_query))
                query = cur.fetchall()
        conn.close()
        return query