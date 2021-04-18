from copom_cal import CopomCalendar
from datetime import date, timedelta
import pytest


@pytest.fixture
def base_case():
    data_inicial = date(2021, 4, 15)
    data_fim = date(2021, 6, 14)
    return CopomCalendar(data_inicial, data_fim)


@pytest.fixture
def has_no_events_case():
    data_inicial = date(2021, 4, 15)
    data_fim = date(2021, 4, 29)
    return CopomCalendar(data_inicial, data_fim)


@pytest.fixture
def unique_date_no_events_case():
    data_inicial = date(2021, 4, 16)
    data_fim = data_inicial
    return CopomCalendar(data_inicial, data_fim)


@pytest.fixture
def unique_date_with_event_case():
    data_inicial = date(2021, 6, 15)
    data_fim = data_inicial
    return CopomCalendar(data_inicial, data_fim)


@pytest.fixture
def next_year_case():
    data_inicial = date.today() + timedelta(days=365)
    data_fim = date.today() + timedelta(days=366)
    return CopomCalendar(data_inicial, data_fim)


@pytest.fixture
def inicio_gt_fim():
    # cenário com data inicial menor que final
    data_fim = date.today()
    data_inicial = data_fim + timedelta(days=1)
    return CopomCalendar(data_inicial, data_fim)


@pytest.fixture
def inicio_apos_calendario_conhecido():
    # cenário com data inicial no futuro
    # 366 + 185 para garantir data de período
    # ainda sem definição de calendário
    # (de acordo com a circular, o calendário do ano
    # seguinte é divulgado até fim de junho
    data_inicial = date.today() + timedelta(days=551)
    data_fim = data_inicial + + timedelta(days=15)
    return CopomCalendar(data_inicial, data_fim)


@pytest.fixture
def datas_none():
    # cenário com datas = None
    data_inicial = None
    data_fim = None
    return CopomCalendar(data_inicial, data_fim)


@pytest.fixture
def inicio_agenda_none():
    # cenário com inicio_agenda = None
    data_inicial = None
    data_fim = date.today()
    return CopomCalendar(data_inicial, data_fim)


@pytest.fixture
def datas_str():
    # cenário com datas = str
    data_inicial = '2021-07-21'
    data_fim = '2021-07-28'
    return CopomCalendar(data_inicial, data_fim)
