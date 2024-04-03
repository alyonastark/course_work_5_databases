import psycopg2
from psycopg2.errors import UniqueViolation


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
        with self.connect:
            with self.connect.cursor() as cursor:
                cursor.execute("CREATE TABLE IF NOT EXISTS employers "
                               "( employer_id varchar PRIMARY KEY, employer_name varchar NOT NULL,"
                               " employer_url varchar NOT NULL )")

                cursor.execute("CREATE TABLE IF NOT EXISTS vacancies"
                               " ( vacancy_id varchar PRIMARY KEY, vacancy_name varchar NOT NULL,"
                               " employer_id varchar, salary_from int,"
                               " salary_to int, vacancy_url varchar NOT NULL,"
                               "CONSTRAINT fk_vacancies_employer_id FOREIGN KEY(employer_id) REFERENCES "
                               "employers(employer_id) )")

    def add_employer(self, employer):
        """Добавляет данные о работодателе в таблицу employees"""
        try:
            with self.connect.cursor() as cursor:
                cursor.execute("INSERT INTO employers VALUES (%s, %s, %s)",
                               (employer['id'], employer['name'], employer['alternate_url']))
        except UniqueViolation:
            print("Эта компания уже добавлена")

    def add_vacancies(self, vacancies):
        """Добавляет данные о вакансиях в таблицу vacancies"""
        try:
            with self.connect.cursor() as cursor:
                for vacancy in vacancies:
                    vacancy_name = vacancy['name'].lower()
                    if vacancy['salary'] is None:
                        salary_from = None
                        salary_to = None
                    else:
                        salary_from = vacancy['salary']['from']
                        salary_to = vacancy['salary']['to']

                    cursor.execute("INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s)",
                                   (vacancy['id'], vacancy_name, vacancy['employer']['id'],
                                    salary_from, salary_to, vacancy['alternate_url']))
        except UniqueViolation:
            print("Эти вакансии уже добавлены")

    def get_companies_and_vacancies_count(self):
        """получает список всех компаний и количество вакансий у каждой компании"""
        with self.connect.cursor() as cursor:
            cursor.execute("SELECT e.employer_name, COUNT(v.vacancy_name) "
                            "FROM employers as e "
                            "JOIN vacancies as v USING(employer_id) "
                            "GROUP BY employer_name")
            rows = cursor.fetchall()
            for row in rows:
                print(row)

    def get_all_vacancies(self):
        """получает список всех вакансий(название компании, вакансии, зарплаты, ссылки на вакансию"""
        with self.connect.cursor() as cursor:
            cursor.execute("SELECT v.vacancy_name, e.employer_name, CONCAT(v.salary_from, '-', v.salary_to) "
                            "AS salary, v.vacancy_url "
                            "FROM vacancies as v "
                            "JOIN employers as e USING(employer_id)")
            rows = cursor.fetchall()
            for row in rows:
                print(row)

    def get_avg_salary(self):
        """Получает среднюю зарплату по всем вакансиям (исключая вакансии где зп не указана)"""
        with self.connect.cursor() as cursor:
            cursor.execute("SELECT AVG ((salary_from + salary_to) / 2) "
                            "FROM vacancies "
                            "WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL")
            result = cursor.fetchall()
            return result

    def get_vacancies_with_higher_salary(self, avg_salary):
        """Получает список вакансий, у которых зп выше средней по всем вакансиям"""
        with self.connect.cursor() as cursor:
            cursor.execute("SELECT * FROM vacancies WHERE (salary_from + salary_to) / 2 > (%s)",
                            avg_salary)
            rows = cursor.fetchall()
            for row in rows:
                print(row)

    def get_vacancies_with_keyword(self, keyword):
        """Получает список вакансий, в названии которых содержится переданные слова"""
        with self.connect.cursor() as cursor:
            sql = "SELECT * FROM vacancies WHERE vacancy_name LIKE %(like)s"
            cursor.execute(sql, {'like': '%' + keyword + '%'})

            rows = cursor.fetchall()
            for row in rows:
                print(row)

    def close_connection(self):
        """Закрывает соединение с бд"""
        return self.connect.close()
