from copom_cal import CopomCalendar
from datetime import date
import pytest


@pytest.fixture
def base_case():
    data_inicial = date(2021, 4, 15)
    data_fim = date(2021, 6, 14)
    return CopomCalendar(data_inicial, data_fim)
