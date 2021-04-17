from datetime import date
import json
import requests


class CopomCalendar:
    def __init__(self, inicio_agenda: date, fim_agenda: date):
        # atribui data de início e fim para o calendário
        self._inicio_agenda, self._fim_agenda = inicio_agenda, fim_agenda
        self._cache = {}
        self._url_base = 'https://www.bcb.gov.br/api/servico/sitebcb/agendas?' \
                         'lista=Reuni%C3%B5es%20do%20Copom&inicioAgenda=%27{data1}%27&fimAgenda=%27{data2}%27'
        self._url = ''
        self._chave_conteudo = 'conteudo'

    def __len__(self):
        self._process_new_request()

        return len(self._cache[self._url])

    def __str__(self):
        self._process_new_request()

        return self._url

    def __getitem__(self, item):
        self._process_new_request()

        return self._cache[self._url][item]

    @property
    def has_new_events(self) -> bool:
        self._process_new_request()

        # retorna se há eventos no período
        return len(self._cache[self._url]) > 0

    @property
    def inicio_agenda(self) -> date:
        return self._inicio_agenda

    @property
    def fim_agenda(self) -> date:
        return self._fim_agenda

    @inicio_agenda.setter
    def inicio_agenda(self, data: date):
        self._inicio_agenda = data

        self._process_new_request()

    @fim_agenda.setter
    def fim_agenda(self, data: date):
        self._fim_agenda = data

        self._process_new_request()

    def _process_new_request(self):
        # verifica se datas estão coerentes (inicio_agenda <= fim_agenda)
        self._check_date_values()

        # url para requisição solicitada
        url = self._url_base.format(data1=self._inicio_agenda.isoformat(),
                                    data2=self._fim_agenda.isoformat())

        # adiciona ao calendário, se necessário
        self._add_calendar(url)

        # url da solicitação
        self._url = url

    def _add_calendar(self, url: str):
        if url not in self._cache.keys():
            response = requests.get(url)

            if response.status_code == 200:
                json_data = json.loads(response.text)
                self._cache[url] = json_data[self._chave_conteudo]

    def _check_date_values(self):
        if not isinstance(self._inicio_agenda, date) and not isinstance(self._fim_agenda, date):
            raise TypeError

        if self._inicio_agenda > self._fim_agenda:
            self._cache[self._url] = {}
