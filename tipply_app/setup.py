# ===============================================================
# Tipply macOS App setup.py
# Copyright (c) 2025 Maglovski Nenad
# Licensed under MIT
# ===============================================================

from setuptools import setup
import os 

brew_prefix = os.popen('brew --prefix tcl-tk').read().strip()

APP = ["main.py"]

OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'images/MyIcon.ico',
    'excludes': ['rubicon', 'rubicon.objc'],
    'packages': ['tkinter', 'customtkinter', 'cmath'], 
    'includes': ['tkinter', 'customtkinter'],
    'frameworks': [
        os.path.join(brew_prefix, 'Frameworks', 'Tcl.framework'),
        os.path.join(brew_prefix, 'Frameworks', 'Tk.framework'),
    ],
    'plist': {
        'CFBundleName': 'Tipply',
        'CFBundleDisplayName': 'Tipply',
        'CFBundleIdentifier': 'com.maglovski.tipply',
        'CFBundleVersion': '0.0.1',
        'CFBundleShortVersionString': '0.0.1',
    },
}

setup(
    name="Tipply",
    version="0.0.1",
    description="A simple way to send and receive digital tips",
    author="Maglovski Nenad",
    author_email="maglovskin@gmail.com",
    url="https://github.com/maglovskiNenad/hopplo",
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
