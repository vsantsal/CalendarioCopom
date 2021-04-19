import pytest
import requests
from unittest.mock import patch
from datetime import date, timedelta
from copom_cal import CopomCalendar


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
                              date.today() + timedelta(days=15), 0),
                         ])
def test_len_cenarios(data_inicial, data_fim, resultado):
    cenario = CopomCalendar(data_inicial, data_fim)
    eventos = len(cenario)
    assert eventos == resultado


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
def test_has_events_cenarios(data_inicial, data_fim, resultado):
    cenario = CopomCalendar(data_inicial, data_fim)
    flag = cenario.has_new_events
    assert flag == resultado


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


def test_has_events_as_dict_base_case(base_case):
    for event in base_case:
        assert isinstance(event, dict)


@patch('requests.get')
def test_connection_error(mock_requests_get, base_case):
    mock_requests_get.side_effect = requests.exceptions.ConnectionError()
    with pytest.raises(ConnectionError):
        len(base_case)
