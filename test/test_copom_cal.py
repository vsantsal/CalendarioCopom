import pytest
from unittest.mock import patch
from datetime import date, timedelta
from copom_cal import CopomCalendar


class StubApi:
    def get_data(self, url: str, chave_outer_dict: dict):
        pass


@patch('src.copom_cal.JsonApi', return_value=StubApi())
@pytest.mark.parametrize("data_inicial, data_fim, resultado",
                         [
                             (date(2021, 4, 15), date(2021, 6, 14), 3),
                             (date(2021, 4, 15), date(2021, 4, 29), 0),
                             (date(2021, 4, 16), date(2021, 4, 16), 0),
                             (date(2021, 6, 15), date(2021, 6, 15), 0),
                             (date.today() + timedelta(days=365),
                              date.today() + timedelta(days=366), 0),
                             (date.today() + timedelta(days=1), date.today(), 0),
                             (date.today() + timedelta(days=551),
                              date.today() + timedelta(days=551) + timedelta(days=15), 0),
                         ])
def test_len_cenarios(stub_api, data_inicial, data_fim, resultado):
    # colocando como retorno range com o número informado
    # para que len(self._get_dados) retorne o esperado
    stub_api.get_data.return_value = range(resultado)
    cenario = CopomCalendar(data_inicial, data_fim, stub_api)
    eventos = len(cenario)
    assert eventos == resultado


@patch('src.copom_cal.JsonApi', return_value=StubApi())
@pytest.mark.parametrize("data_inicial, data_fim, resultado",
                         [
                             (date(2021, 4, 15), date(2021, 6, 14), True),
                             (date(2021, 4, 15), date(2021, 4, 29), False),
                             (date(2021, 4, 16), date(2021, 4, 16), False),
                             (date(2021, 6, 15), date(2021, 6, 15), False),
                             (date.today() + timedelta(days=365),
                              date.today() + timedelta(days=366), False),
                             (date.today() + timedelta(days=1), date.today(), False),
                             (date.today() + timedelta(days=551),
                              date.today() + timedelta(days=15), False),
                         ])
def test_has_events_cenarios(stub_api, data_inicial, data_fim, resultado):
    stub_api.get_data.return_value = range(resultado)
    cenario = CopomCalendar(data_inicial, data_fim)
    flag = cenario.has_new_events
    assert flag == resultado


@pytest.mark.parametrize("data_inicial, data_fim, resultado",
                         [
                             (date(2021, 4, 15), date(2021, 6, 14), date(2021, 4, 15)),
                             (date(2021, 4, 15), date(2021, 4, 29), date(2021, 4, 15)),
                             (date(2021, 4, 16), date(2021, 4, 16), date(2021, 4, 16)),
                             (date(2021, 6, 15), date(2021, 6, 15), date(2021, 6, 15)),
                             (date.today() + timedelta(days=365),
                              date.today() + timedelta(days=366),
                              date.today() + timedelta(days=365)),
                             (date.today() + timedelta(days=1), date.today(),
                              date.today() + timedelta(days=1)),
                             (date.today() + timedelta(days=551),
                              date.today() + timedelta(days=15),
                              date.today() + timedelta(days=551)),
                         ])
def test_inicio_agenda_getter(data_inicial, data_fim, resultado):
    cenario = CopomCalendar(data_inicial, data_fim)
    inicio_agenda = cenario.inicio_agenda
    assert inicio_agenda == resultado


@pytest.mark.parametrize("data_inicial, data_fim, resultado",
                         [
                             (date(2021, 4, 15), date(2021, 6, 14), date(2020, 12, 17)),
                             (date(2021, 4, 15), date(2021, 4, 29), date(2021, 1, 15)),
                             (date(2021, 4, 16), date(2021, 4, 16), date(2021, 4, 15)),
                             (date(2021, 6, 15), date(2021, 6, 15), date(2019, 3, 13)),
                             (date.today() + timedelta(days=365),
                              date.today() + timedelta(days=366),
                              date.today() + timedelta(days=366)),
                             (date.today() + timedelta(days=1), date.today(),
                              date.today() + timedelta(days=2)),
                             (date.today() + timedelta(days=551),
                              date.today() + timedelta(days=15),
                              date.today() + timedelta(days=16)),
                         ])
def test_inicio_agenda_setter(data_inicial, data_fim, resultado):
    cenario = CopomCalendar(data_inicial, data_fim)
    cenario.inicio_agenda = resultado
    inicio_agenda = cenario.inicio_agenda
    assert inicio_agenda == resultado


@pytest.mark.parametrize("data_inicial, data_fim, resultado",
                         [
                             (date(2021, 4, 15), date(2021, 6, 14), date(2021, 6, 14)),
                             (date(2021, 4, 15), date(2021, 4, 29), date(2021, 4, 29)),
                             (date(2021, 4, 16), date(2021, 4, 16), date(2021, 4, 16)),
                             (date(2021, 6, 15), date(2021, 6, 15), date(2021, 6, 15)),
                             (date.today() + timedelta(days=365),
                              date.today() + timedelta(days=366),
                              date.today() + timedelta(days=366)),
                             (date.today() + timedelta(days=1), date.today(),
                              date.today()),
                             (date.today() + timedelta(days=551),
                              date.today() + timedelta(days=15),
                              date.today() + timedelta(days=15)),
                         ])
def test_fim_agenda_getter(data_inicial, data_fim, resultado):
    cenario = CopomCalendar(data_inicial, data_fim)
    fim_agenda = cenario.fim_agenda
    assert fim_agenda == resultado


@pytest.mark.parametrize("data_inicial, data_fim, resultado",
                         [
                             (date(2021, 4, 15), date(2021, 6, 14), date(2021, 7, 14)),
                             (date(2021, 4, 15), date(2021, 4, 29), date(2021, 9, 30)),
                             (date(2021, 4, 16), date(2021, 4, 16), date(2021, 5, 16)),
                             (date(2021, 6, 15), date(2021, 6, 15), date(2022, 2, 15)),
                             (date.today() + timedelta(days=365),
                              date.today() + timedelta(days=366),
                              date.today() + timedelta(days=367)),
                             (date.today() + timedelta(days=1), date.today(),
                              date.today() + timedelta(days=-11)),
                             (date.today() + timedelta(days=551),
                              date.today() + timedelta(days=15),
                              date.today() + timedelta(days=21)),
                         ])
def test_fim_agenda_setter(data_inicial, data_fim, resultado):
    cenario = CopomCalendar(data_inicial, data_fim)
    cenario.fim_agenda = resultado
    fim_agenda = cenario.fim_agenda
    assert fim_agenda == resultado


@pytest.mark.parametrize("data_inicial, data_fim",
                         [
                             (None, date(2021, 6, 14)),
                             (None, None),
                             ('2021-07-15', '2021-08-15'),
                         ])
def test_has_events_raises_type_error(data_inicial, data_fim):
    with pytest.raises(TypeError):
        cenario = CopomCalendar(data_inicial, data_fim)
        cenario.has_new_events


@pytest.mark.parametrize("data_inicial, data_fim",
                         [
                             (None, date(2021, 6, 14)),
                             (None, None),
                             ('2021-07-15', '2021-08-15'),
                         ])
def test_len_raises_type_error(data_inicial, data_fim):
    with pytest.raises(TypeError):
        cenario = CopomCalendar(data_inicial, data_fim)
        len(cenario)


@patch('src.copom_cal.JsonApi', return_value=StubApi())
def test_has_events_as_dict_base_case(stub_api):
    stub_api.get_data.return_value = [{'1': 1}, {'2': 2}, {'3': 3}]
    cenario = CopomCalendar(date(2021, 4, 15), date(2021, 6, 14), stub_api)
    for event in cenario:
        assert isinstance(event, dict)


@patch('src.copom_cal.JsonApi', return_value=StubApi())
def test_connection_error(stub_api_erro_requests):
    stub_api_erro_requests.get_data.side_effect = ConnectionError
    data_inicial = date(2021, 4, 15)
    data_fim = date(2021, 6, 14)
    caso = CopomCalendar(data_inicial, data_fim, stub_api_erro_requests)
    with pytest.raises(ConnectionError):
        len(caso)
