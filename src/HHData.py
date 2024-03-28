import requests
import json


class HHData:
    """Класс для работы с hh.ru"""

    def __init__(self):
        pass

    def get_employees(self, search_query):
        """Получает список работодателей"""
        response = requests.get('https://api.hh.ru/employers',
                                {'text': search_query, 'area': 113,
                                 'per page': 20, 'only with vacancies': True,
                                 'sort by': 'by_vacancies_open'})
        employees = json.loads(response.text)['items']
        return employees

    def get_vacancies(self, employee):
        """Получает список вакансий"""
        url = employee['vacancies_url']
        response_vacancies = requests.get(url)
        vacancies = json.loads(response_vacancies.text)['items']
        return vacancies

