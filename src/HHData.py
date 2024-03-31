import requests
import json


class HHData:
    """Класс для работы с hh.ru"""

    def __init__(self):
        pass

    def get_employers(self, search_query):
        """Получает список работодателей"""
        response = requests.get('https://api.hh.ru/employers',
                                {'text': search_query, 'area': 113,
                                 'per page': 100, 'only with vacancies': True,
                                 'sort_by': 'by_vacancies_open'})
        employers = json.loads(response.text)['items']
        return employers

    def get_vacancies(self, employer):
        """Получает список вакансий"""
        url = employer['vacancies_url']
        response_vacancies = requests.get(url)
        vacancies = json.loads(response_vacancies.text)['items']
        return vacancies




