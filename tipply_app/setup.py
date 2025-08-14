# ===============================================================
# Tipply macOS App setup.py
# Copyright (c) 2025 Maglovski Nenad
# Licensed under MIT
# ===============================================================

from setuptools import setup

APP = ["main.py"]

OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'images/MyIcon.ico',
    'includes': ['jaraco.text', 'jaraco.classes', 'jaraco.collections', 'rubicon.objc'],
    'packages': ['jaraco.text', 'jaraco.classes', 'jaraco.collections', 'rubicon.objc'],
    'skip_archive': True,
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
