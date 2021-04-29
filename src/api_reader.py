from abc import ABC, abstractmethod
import requests


class RestApi(ABC):
    @abstractmethod
    def get_data(self, *args):
        """método para retorno de dados."""


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
                response = requests.get(self._url).json()

            except requests.exceptions.ConnectionError:
                print("Unnable to connect to {}".format(self._url))
                raise ConnectionError
            else:
                self._cache[self._url] = response[self._chave_outer_dict] \
                    if self._chave_outer_dict \
                    else response
