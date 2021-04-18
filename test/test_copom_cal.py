import pytest
import requests
from unittest.mock import patch

def test_len_base_case_is_3(base_case):
    eventos = len(base_case)
    assert eventos == 3


def test_has_events_base_case_is_ok(base_case):
    flag = base_case.has_new_events
    assert flag


def test_len_inicio_gt_fim_ok(inicio_gt_fim):
    eventos = len(inicio_gt_fim)
    assert eventos == 0


def test_has_events_has_no_events_case_is_false(has_no_events_case):
    flag = has_no_events_case.has_new_events
    assert not flag


def test_len_has_no_events_case_is_0(has_no_events_case):
    eventos = len(has_no_events_case)
    assert eventos == 0


def test_has_events_unique_date_no_events_case_is_false(unique_date_no_events_case):
    flag = unique_date_no_events_case.has_new_events
    assert not flag


def test_len_unique_date_no_events_case_is_0(unique_date_no_events_case):
    eventos = len(unique_date_no_events_case)
    assert eventos == 0


def test_has_events_unique_date_with_event_case_is_false(unique_date_with_event_case):
    flag = unique_date_with_event_case.has_new_events
    assert not flag


def test_len_unique_with_event_case_is_0(unique_date_with_event_case):
    eventos = len(unique_date_with_event_case)
    assert eventos == 0


def test_has_events_next_year_case_is_false(next_year_case):
    flag = next_year_case.has_new_events
    assert not flag


def test_len_next_year_case_is_zero(next_year_case):
    eventos = len(next_year_case)
    assert eventos == 0


def test_has_events_as_dict_base_case(base_case):
    for event in base_case:
        assert isinstance(event, dict)


def test_has_events_inicio_apos_calendario_conhecido_is_false(inicio_apos_calendario_conhecido):
    flag = inicio_apos_calendario_conhecido.has_new_events
    assert not flag


def test_len_inicio_apos_calendario_conhecido_is_zero(inicio_apos_calendario_conhecido):
    eventos = len(inicio_apos_calendario_conhecido)
    assert eventos == 0


def test_has_events_datas_none_raises_type_error(datas_none):

    with pytest.raises(TypeError):
        datas_none.has_new_events


def test_len_datas_none_raises_type_error(datas_none):
    with pytest.raises(TypeError):
        len(datas_none)


def test_has_events_inicio_agenda_none_raises_type_error(inicio_agenda_none):
    with pytest.raises(TypeError):
        inicio_agenda_none.has_new_events


def test_len_inicio_agenda_none_raise_type_error(inicio_agenda_none):
    with pytest.raises(TypeError):
        len(inicio_agenda_none)


def test_has_events_datas_str_raises_type_error(datas_str):
    with pytest.raises(TypeError):
        datas_str.has_new_events


def test_len_datas_str_raises_type_error(datas_str):
    with pytest.raises(TypeError):
        len(datas_str)


@patch('requests.get')
def test_connection_error(mock_requests_get, base_case):
    mock_requests_get.side_effect = requests.exceptions.ConnectionError()
    with pytest.raises(ConnectionError):
        len(base_case)