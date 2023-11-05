import json
from abc import ABC

import requests

from vacancy_api import VacancyAPI


class HeadHunterAPI(VacancyAPI, ABC):
    """Создаем класс для получения вакансий с сайта HeadHunter"""
    url = 'https://api.hh.ru/vacancies'
    header = {'User-Agent': 'Myapp'}
    filename = 'hh_vacancy.json'

    def __init__(self, keyword=None):
        self.params = {'text': keyword}

    def get_response(self):
        """Отправляем запрос на API для получения вакансий в JSON"""
        response = requests.get(self.url, headers=self.header, params=self.params)
        return response.json()['items']

    def save_to_file(self, data, filename):
        """Сохраняем полученные данные в необходимом формате"""
        self.filename = filename
        with open(self.filename, 'w', encoding='utf-8') as file:
            data_list = []
            for dict_ in data:
                temp_dict = {'name': dict_['name'], 'area': dict_['area']['name'],
                             'salary': dict_.get('salary'), 'url': dict_['alternate_url'],
                             'requirement': dict_['snippet']['requirement']}
                data_list.append(temp_dict)
            json.dump(data_list, file, ensure_ascii=False, indent=2)
