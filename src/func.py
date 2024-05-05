import psycopg2


def proc_company_data(companies=[]) -> list:
    """
    Функция для упрощения полученных данных компаний
    """

    companies_list = []
    for el in companies:
        companies_list.append({'employer_id': el['id'],
                               'name': el['name'],
                               'url': el['alternate_url'],
                               'vacancies_url': el['vacancies_url'],
                               'open_vacancies': el['open_vacancies']})
    return companies_list


def proc_vacs_data(vacs=[]) -> list:
    """
    Функция для упрощения полученных данных вакансий
    """
    vacs_list = []
    for el in vacs:
        if el['salary']['from'] is None:
            salary = el['salary']['to']
        else:
            salary = el['salary']['from']
        vacs_list.append({'vacancy_id': el['id'],
                          'name': el['name'],
                          'city': el['area']['name'],
                          'description': el['snippet']['responsibility'],
                          'url': el['alternate_url'],
                          'salary': salary,
                          'requirement': el['snippet']['requirement'],
                          'employer_id': el['employer']['id'],
                          'employer_name': el['employer']['name']})
    return vacs_list


def create_database(database_name: str, params: dict) -> None:
    """
    Создание базы данных и таблиц для сохранения данных о компаниях их вакансиях.
    """
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    try:
        cur.execute(f"DROP DATABASE {database_name}")

    except Exception as e:
        print(f'Информация: {e}')

    finally:

        cur.execute(f"CREATE DATABASE {database_name}")
        print(f'База данных {database_name} создана')

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers (
                employers_id VARCHAR(50) UNIQUE NOT NULL,
                employers_name VARCHAR(255) NOT NULL,
                employers_url TEXT,
                open_vacancies INTEGER,

                CONSTRAINT pk_employers_employers_id PRIMARY KEY (employers_id)
            )""")

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancies_id VARCHAR(50) NOT NULL,
                vacancy_name VARCHAR(255) NOT NULL,
                city VARCHAR(50) NOT NULL,
                description TEXT,
                url TEXT,
                salary INTEGER,
                requirement TEXT,
                employers_id VARCHAR(50) NOT NULL,
                employers_name VARCHAR(255) NOT NULL,

                CONSTRAINT pk_vacancies_vacancies_id PRIMARY KEY (vacancies_id)
            );
            """)

    conn.commit()
    conn.close()


def save_data_employers_to_database(data: list, database_name: str, params: dict) -> None:
    """
    Функция для сохранения данных о каналах и вакансиях в базу данных.
    """
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for employer in data:
            cur.execute("""
            INSERT INTO employers (employers_id, employers_name, employers_url, open_vacancies)
            VALUES (%s, %s, %s, %s)
            """,
                        (
                            employer.get('employer_id'),
                            employer.get('name'),
                            employer.get('url'),
                            employer.get('open_vacancies')
                        ))
    conn.commit()
    conn.close()


def save_data_vacancies_to_database(data: list, database_name: str, params: dict) -> None:
    """
    Функция для сохранения данных о вакансиях в базу данных.
    """
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        for vacancy in data:
            cur.execute("""
            INSERT INTO vacancies (vacancies_id, 
            vacancy_name, 
            city, 
            description,
            url, 
            salary, 
            requirement, 
            employers_id, 
            employers_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
                        (
                            vacancy.get('vacancy_id'),
                            vacancy.get('name'),
                            vacancy.get('city'),
                            vacancy.get('description'),
                            vacancy.get('url'),
                            vacancy.get('salary'),
                            vacancy.get('requirement'),
                            vacancy.get('employer_id'),
                            vacancy.get('employer_name')
                        ))
    conn.commit()
    conn.close()