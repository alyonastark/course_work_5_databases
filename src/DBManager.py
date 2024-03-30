import psycopg2


class DBManager:
    """Класс для работы с базами данных"""

    def __init__(self):
        """Инициализатор класса, создает таблицы employees и vacancies"""
        self.connect = psycopg2.connect(
            host='localhost',
            database='employers and vacancies',
            user='postgres',
            password='Miracle13/'
        )
        try:
            with self.connect:
                with self.connect.cursor() as cursor:
                    cursor.execute("CREATE TABLE employers "
                                   "( employer_id varchar PRIMARY KEY, employer_name varchar NOT NULL,"
                                   " employer_url varchar NOT NULL )")

                    cursor.execute("CREATE TABLE vacancies"
                                   " ( vacancy_id varchar PRIMARY KEY, vacancy_name varchar NOT NULL,"
                                   " employer_id REFERENCES employers(employer_id), salary_from int,"
                                   " salary_to int, vacancy_url varchar NOT_NULL )")

        finally:
            self.connect.close()

    def add_emloyee(self, employer):
        """Добавляет данные о работодателе в таблицу employees"""
        try:
            with self.connect:
                with self.connect.cursor() as cursor:
                    cursor.execute("INSERT INTO employers VALUES (%s, %s, %s)",
                                   (employer['id'], employer['name'], employer['alternate_url']))
        finally:
            self.connect.close()

    def add_vacancies(self, vacancies):
        """Добавляет данные о вакансиях в таблицу vacancies"""
        try:
            with self.connect:
                with self.connect.cursor as cursor:
                    for vacancy in vacancies:
                        vacancy_name = vacancy['name'].lower()
                        if vacancy['salary'] is None:
                            salary_from = None
                            salary_to = None
                        elif vacancy['salary']['to'] is None:
                            salary_to = None
                        elif vacancy['salary']['from'] is None:
                            salary_from = None
                        else:
                            salary_from = vacancy['salary']['from']
                            salary_to = vacancy['salary']['to']

                        cursor.execute("INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s)",
                                       (vacancy['id'], vacancy_name, vacancy['employer']['id'],
                                        salary_from, salary_to, vacancy['alternate_url']))
        finally:
            self.connect.close()

    def get_companies_and_vacancies_count(self):
        """получает список всех компаний и количество вакансий у каждой компании"""
        try:
            with self.connect:
                with self.connect.cursor() as cursor:
                    cursor.execute("SELECT e.employer_name, COUNT(v.vacancy_name)"
                                   "FROM employers as e"
                                   "JOIN vacancies as v USING(employer_id"
                                   "GROUP BY employer_name")
                    rows = cursor.fetchall()
                    for row in rows:
                        print(row)

        finally:
            self.connect.close()

    def get_all_vacancies(self):
        """получает список всех вакансий(название компании, вакансии, зарплаты, ссылки на вакансию"""
        try:
            with self.connect:
                with self.connect.cursor() as cursor:
                    cursor.execute("SELECT v.vacancy_name, e.employer_name, CONCAT(v.salary_from, '-', v.salary_to) "
                                   "AS salary, v.vacancy_url"
                                   "FROM vacancies as v"
                                   "JOIN employers as e USING(employer_id)")
                    rows = cursor.fetchall()
                    for row in rows:
                        print(row)
        finally:
            self.connect.close()

    def get_avg_salary(self):
        """Получает среднюю зарплату по всем вакансиям (исключая вакансии где зп не указана)"""
        try:
            with self.connect:
                with self.connect.cursor() as cursor:
                    cursor.execute("SELECT AVG ((salary_from + salary_to) / 2)"
                                   "FROM vacancies"
                                   "WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL")
                    result = cursor.fetchall()
                    print(result)
        finally:
            self.connect.close()

    def get_vacancies_with_higher_salary(self, avg_salary):
        """Получает список вакансий, у которых зп выше средней по всем вакансиям"""
        try:
            with self.connect:
                with self.connect.cursor() as cursor:
                    cursor.execute("SELECT * FROM vacancies WHERE ((salary_from + salary_to) / 2 > VALUES (%S)",
                                   avg_salary)
                    result = cursor.fetchall()
                    print(result)
        finally:
            self.connect.close()

    def get_vacancies_with_keyword(self, keyword):
        """Получает список вакансий, в названии которых содержится переданные слова"""
        try:
            with self.connect:
                with self.connect.cursor() as cursor:
                    search_query = keyword.lower()
                    cursor.execute("SELECT * INTO search FROM vacancies WHERE vacancy_name LIKE 'VALUES (%S)%';"
                                   "INSERT INTO search SELECT * FROM vacancies WHERE vacancy_name LIKE '%VALUES (%S)%';"
                                   "INSERT INTO search SELECT * FROM vacancies WHERE vacancy_name LIKE 'VALUES (%S)%'",
                                   search_query)
                    result = cursor.fetchall()
                    print(result)

                    cursor.execute("DROP TABLE search")
        finally:
            self.connect.close()
