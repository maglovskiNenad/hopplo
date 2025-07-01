import requests
import subprocess
import os
import sys
import tempfile
import customtkinter as ctk
from warning_msg import WarningPopup

GITHUB_REPO = "maglovskiNenad/hopplo"
LOCALE_VERSION_FILE = "version.txt"

# TODO potraziti lokalnu verziju
def get_local_version():
    with open(LOCALE_VERSION_FILE,"r")as f:
        return  f.read().strip()

# TODO potraziti poslednju verziju

# TODO download dmg fajla za instalaciju

# TODO mount i instalacija

# TODO poslati ga u main

