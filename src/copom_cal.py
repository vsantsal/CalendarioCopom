from datetime import date
import json
import requests


class CopomCalendar:
    def __init__(self, inicio_agenda: date, fim_agenda: date):
        # atribui data de início e fim para o calendário
        self._inicio_agenda, self._fim_agenda = inicio_agenda, fim_agenda
        # verifica se datas estão coerentes (inicio_agenda <= fim_agenda)
        self._check_date_values()

        self._cache = {}
        self._url_base = 'https://www.bcb.gov.br/api/servico/sitebcb/agendas?' \
                         'lista=Reuni%C3%B5es%20do%20Copom&inicioAgenda=%27{data1}%27&fimAgenda=%27{data2}%27'
        self._url = ''
        self._chave_conteudo = 'conteudo'

    @property
    def events(self):
        return self._cache[self._url]

    def has_events(self) -> bool:

        self._process_new_request()

        # retorna se há eventos no período
        return len(self._cache[self._url]) > 0

    def number_of_events(self) -> int:

        self._process_new_request()

        return len(self._cache[self._url])

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
            if self._inicio_agenda == self._fim_agenda:
                self._cache[url] = {}
            else:
                response = requests.get(url)

                if response.status_code == 200:
                    json_data = json.loads(response.text)
                    self._cache[url] = json_data[self._chave_conteudo]

    def _check_date_values(self):
        if self._inicio_agenda > self._fim_agenda:
            raise ValueError('{data1} must be less than or equal to {data2}'.
                             format(data1=self._inicio_agenda.isoformat(),
                                    data2=self._fim_agenda.isoformat()))


if __name__ == '__main__':
    cal_copom = CopomCalendar(inicio_agenda=date(2021, 4, 15), fim_agenda=date(2021, 6, 15))
    print(cal_copom.has_events())
    print(cal_copom.number_of_events())
    for event in cal_copom.events:
        print('Evento: {}'.format(event['evento']))
        print('Data: {}\n'.format(event['dataEvento']))
