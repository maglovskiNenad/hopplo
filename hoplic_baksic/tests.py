import pandas as pd
import pytest
from trinkgeld_actions import TrinkgeldActions
from home_page import HomePage
from warning_msg import WarningPopup
from  main import App,SidebarFrame,MainFrame


@pytest.fixture
def trinkgeld_obj():
    return TrinkgeldActions(None)

def test_extract_confirmed_work_hours(trinkgeld_obj):
    test_data = pd.DataFrame({
        "tag": ["01.06.2024", "01.06.2024", "02.06.2024", "02.06.2024"],
        "vorname":["Ana", "Marko", "Ana", "Ivan"],
        "dauerbruttodezimal": ["4,5", "3", "5", "x"],
        "typ": ["Bestätigte Arbeitszeit", "Bestätigte Arbeitszeit", "Unbestätigte Arbeitszeit","Bestätigte Arbeitszeit"],
        "arbeitsbereich": ["Barista", "Barista", "Barista", "Barista"]
    })

    result = trinkgeld_obj.extract_confirmed_work_hours(test_data)

    expected = {
        "Ana": {
            "01.06.": 4.5
        },
        "Marko": {
            "01.06.": 3.0
        },
        "Ivan": {
            "02.06.": 0.0
        }
    }

    assert result == expected