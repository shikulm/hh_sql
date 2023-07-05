from abc import ABC

import httpx
from exceptions.api_exception import HHApiError
from config import hh_api_config


from get_api.abstract_get_api import AbstractGetApi


# class GetApiHh(AbstractGetApi):
class GetApiHh():

    def __init__(self, page: int = 0):

        self.url = "https://api.hh.ru/vacancies"
        self.params = {
            "page": page,
            "employer_id": hh_api_config.get('emplloyer_id'),
            "only_with_salary": hh_api_config.get('only_with_salary'),
            "per_page": hh_api_config.get('vacancies_per_page'),
            "area": hh_api_config.get('area')
        }

    def get_vacancies(self) -> list[dict]:
        response = httpx.get(url=self.url, params = self.params)
        if response.status_code != 200:
            raise HHApiError(f"Error type: {response.json()['errors'][0]['type']}, "
                            f"Status code {response.status_code}")
        return [
            {
                'id_vacancy': el.get('id'),
                'name_vacancy': el.get('name'),
                'id_employer': el['employer'].get('id'),
                'city': el['area'].get('name'),
                'salary_from': el['salary'].get('from'),
                'salary_to': el['salary'].get('to'),
                'requirement': el['snippet'].get('requirement'),
                'responsibility': el['snippet'].get('responsibility')

            } for el in response.json()['items']
        ]
        # return response.json()['items']


    def get_employer(self) -> list[dict]:
        return [
            {
                'id_employer': uid,
                'name': httpx.get(f"https://api.hh.ru/employers/{uid}").json().get('name'),
                'url': httpx.get(f"https://api.hh.ru/employers/{uid}").json().get('alternate_url')
            } for uid in self.params.get('employer_id') if uid is not None
        ]


hh = GetApiHh()
# print(hh.get_employer())
print(hh.get_vacancies())
