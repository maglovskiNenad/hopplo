# ===============================================================
# CSV reader
# Copyright (c) 2025 Maglovski Nenad
# This source code is licensed under the MIT
# license found in the LICENSE file.
# ===============================================================

import pandas as pd
import pytest
from trinkgeld_actions import TrinkgeldActions
from home_page import HomePage
from warning_msg import WarningPopup
from  main import App,SidebarFrame,MainFrame
import os
import tempfile


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

def text_load_and_clean_csv_data(trinkgeld_obj):
    content = "  \ufeffVORNAME ; DAUERBRUTTO_DEZIMAL \nAna;4,5\nMarko;3"

    with tempfile.NamedTemporaryFile("w+",delete=False,suffix=".csv",encoding="utf-8")as tmpfile:
        tmpfile.write(content)
        tmpfile_path =(tmpfile.name)

    df = trinkgeld_obj.load_and_clean_csv_data(tmpfile_path,delimiter=";")

    os.remove(tmpfile_path)

    expected_columns = ["vorname","dauerbruttodezimal"]

    assert list(df.columns) == expected_columns
    assert df.shape == (2,2)
    assert df.iloc[0,0] == "Ana"
    assert df.iloc[1,1] == "3"

def test_clean_list_data(trinkgeld_obj):
    pass

def test_display_and_clean_daily_tip(trinkgeld_obj):
    pass

def test_get_hourly_tip(trinkgeld_obj):
    pass

def test_calculation_merging_two_lists(trinkgeld_obj):
    pass

def test_calculation_merging_two_lists(trinkgeld_obj):
    pass

def test_display_file_path(trinkgeld_obj):
    pass

def test_handle_drop(trinkgeld_obj):
    pass

def test_screenshot_widget(trinkgeld_obj):
    pass
