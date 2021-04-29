from datetime import date
from api_reader import JsonApi


class CopomCalendar:
    def __init__(self, inicio_agenda: date, fim_agenda: date, api=JsonApi()):
        # atribui data de início e fim para o calendário
        self._inicio_agenda, self._fim_agenda = inicio_agenda, fim_agenda
        self._url = ''
        self._bacen_api = api
        self._chave_conteudo = 'conteudo'

    def __len__(self):
        self._set_dados()
        return len(self._dados)

    def __str__(self):
        return self._url

    def __getitem__(self, item):
        self._set_dados()
        return self._dados[item]

    @property
    def has_new_events(self) -> bool:
        self._set_dados()
        # retorna se há eventos no período
        return len(self._dados) > 0

    @property
    def inicio_agenda(self) -> date:
        return self._inicio_agenda

    @property
    def fim_agenda(self) -> date:
        return self._fim_agenda

    @inicio_agenda.setter
    def inicio_agenda(self, data: date):
        self._inicio_agenda = data

    @fim_agenda.setter
    def fim_agenda(self, data: date):
        self._fim_agenda = data

    def _set_dados(self):
        self._url = self._set_url_api()
        if self._check_date_values():
            self._dados = self._bacen_api.get_data(self._url, self._chave_conteudo)
        else:
            self._dados = {}

    def _check_date_values(self) -> bool:
        return self._inicio_agenda < self._fim_agenda

    def _set_url_api(self) -> str:

        url = 'https://www.bcb.gov.br/api/servico/sitebcb/agendas?' \
              'lista=Reuni%C3%B5es%20do%20Copom&inicioAgenda=%27{data1}%27&fimAgenda=%27{data2}%27'

        try:
            # url para requisição solicitada
            return url.format(data1=self._inicio_agenda.isoformat(),
                              data2=self._fim_agenda.isoformat())
        except AttributeError:
            raise TypeError("{} and {} must both be date!".
                            format(self._inicio_agenda, self.fim_agenda))
