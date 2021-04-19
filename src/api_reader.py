import requests
import json


class JsonApi:
    def __init__(self):
        self._url = ''
        self._chave_outer_dict = ''
        self._cache = {}

    def get_data(self, url: str, chave_outer_dict: str = ''):
        self._url = url
        self._chave_outer_dict = chave_outer_dict
        self._get_dict_de_json()
        return self._cache[self._url]

    def _get_dict_de_json(self):

        if self._url not in self._cache.keys():

            try:
                response = requests.get(self._url)

                if response.status_code == 200:
                    json_data = json.loads(response.text)

                    self._cache[self._url] = json_data[self._chave_outer_dict] \
                        if self._chave_outer_dict \
                        else json_data

            except requests.exceptions.ConnectionError:
                print("Unnable to connect to {}".format(self._url))
                raise ConnectionError
