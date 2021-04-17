from src.copom_cal import CopomCalendar
from datetime import date, timedelta
import requests
from unittest.mock import patch
import unittest


class CopomCalendarTest(unittest.TestCase):
    def setUp(self) -> None:
        # cenário básico: apenas uma renião do copom
        # com 3 eventos (2 reuniões + 1 ata)
        # no intervalo fechado
        data_inicial = date(2021, 4, 15)
        data_fim = date(2021, 6, 14)
        self._base_case = CopomCalendar(data_inicial, data_fim)
        # cenário sem eventos: nenhum evento
        # no intervalo fechado
        data_inicial = date(2021, 4, 15)
        data_fim = date(2021, 4, 29)
        self._has_no_events_case = CopomCalendar(data_inicial, data_fim)
        # cenário em que a primeira data e a segunda são iguais
        # {api do banco central não retorna resultado nesse caso}
        # e não temos eventos - testar que não temos resultado
        data_inicial = date(2021, 4, 16)
        data_fim = data_inicial
        self._unique_date_no_event_case = CopomCalendar(data_inicial, data_fim)
        # cenário em que a primeira data e a segunda são iguais
        # e temos evento nela - testar que não temos resultado
        data_inicial = date(2021, 6, 15)
        data_fim = data_inicial
        self._unique_date_with_event_case = CopomCalendar(data_inicial, data_fim)
        # cenário com datas no ano seguinte (sem calendário ainda)
        data_inicial = date.today() + timedelta(days=365)
        data_fim = date.today() + timedelta(days=366)
        self._next_year_case = CopomCalendar(data_inicial, data_fim)
        # cenário com data inicial menor que final
        data_fim = date.today()
        data_inicial = data_fim + timedelta(days=1)
        self._inicio_gt_fim = CopomCalendar(data_inicial, data_fim)
        # cenário com data inicial no futuro
        # 366 + 185 para garantir data de período
        # ainda sem definição de calendário
        # (de acordo com a circular, o calendário do ano
        # seguinte é divulgado até fim de junho
        data_inicial = date.today() + timedelta(days=551)
        data_fim = data_inicial + + timedelta(days=15)
        self._inicio_apos_calendario_conhecido = CopomCalendar(data_inicial, data_fim)
        # cenário com datas = None
        data_inicial = None
        data_fim = None
        self._datas_none = CopomCalendar(data_inicial, data_fim)
        # cenário com inicio_agenda = None
        data_inicial = None
        data_fim = date.today()
        self._inicio_agenda_none = CopomCalendar(data_inicial, data_fim)
        # cenário com datas = str
        data_inicial = '2021-07-21'
        data_fim = '2021-07-28'
        self._datas_str = CopomCalendar(data_inicial, data_fim)

    def tearDown(self) -> None:
        pass

    def test_has_events_inicio_gt_fim_is_false(self):
        flag = self._inicio_gt_fim.has_new_events
        self.assertFalse(flag)

    def test_len_inicio_gt_fim_ok(self):
        eventos = len(self._inicio_gt_fim)
        self.assertEqual(0, eventos)

    def test_has_events_base_case_is_ok(self):
        flag = self._base_case.has_new_events
        self.assertTrue(flag)

    def test_len_base_case_is_zero(self):
        eventos = len(self._base_case)
        self.assertEqual(3, eventos)

    def test_has_events_has_no_events_case_is_false(self):
        flag = self._has_no_events_case.has_new_events
        self.assertFalse(flag)

    def test_len_has_no_events_case_is_zero(self):
        eventos = len(self._has_no_events_case)
        self.assertEqual(0, eventos)

    def test_has_events_unique_date_no_events_case_is_false(self):
        flag = self._unique_date_no_event_case.has_new_events
        self.assertFalse(flag)

    def test_len_unique_date_no_events_case_is_zero(self):
        eventos = len(self._unique_date_no_event_case)
        self.assertEqual(0, eventos)

    def test_has_events_unique_date_with_event_case_is_false(self):
        flag = self._unique_date_with_event_case.has_new_events
        self.assertFalse(flag)

    def test_len_unique_with_event_case_is_0(self):
        eventos = len(self._unique_date_with_event_case)
        self.assertEqual(0, eventos)

    def test_has_events_next_year_case_is_false(self):
        flag = self._next_year_case.has_new_events
        self.assertFalse(flag)

    def test_len_next_year_case_is_zero(self):
        eventos = len(self._next_year_case)
        self.assertEqual(0, eventos)

    def test_has_events_as_dict_base_case(self):
        for event in self._base_case:
            self.assertIsInstance(event, dict)

    def test_has_events_inicio_apos_calendario_conhecido_is_false(self):
        flag = self._inicio_apos_calendario_conhecido.has_new_events
        self.assertFalse(flag)

    def test_len_inicio_apos_calendario_conhecido_is_zero(self):
        eventos = len(self._inicio_apos_calendario_conhecido)
        self.assertEqual(0, eventos)

    def test_has_events_datas_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            flag = self._datas_none.has_new_events

    def test_len_datas_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            eventos = len(self._datas_none)

    def test_inicio_agenda_datas_none_is_none(self):
        self.assertIsNone(self._datas_none.inicio_agenda)

    def test_fim_agenda_datas_none_is_none(self):
        self.assertIsNone(self._datas_none.fim_agenda)

    def test_has_events_inicio_agenda_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            flag = self._inicio_agenda_none.has_new_events

    def test_len_inicio_agenda_none_raise_type_error(self):
        with self.assertRaises(TypeError):
            eventos = len(self._inicio_agenda_none)

    @patch('requests.get')
    def test_connection_error(self, mock_requests_get):
        mock_requests_get.side_effect = requests.exceptions.ConnectionError()
        with self.assertRaises(ConnectionError):
            eventos = len(self._base_case)

    def test_has_events_datas_str_raises_type_error(self):
        with self.assertRaises(TypeError):
            flag = self._datas_str.has_new_events

    def test_len_datas_str_raises_type_error(self):
        with self.assertRaises(TypeError):
            eventos = len(self._datas_str)