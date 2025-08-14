# ===============================================================
# CSV reader
# Copyright (c) 2025 Maglovski Nenad
# This source code is licensed under the MIT
# license found in the LICENSE file.
# ===============================================================

import setuptools
from setuptools import setup

APP = ["main.py"]
OPTIONS = {
    'argv_emulation': True,
    'packages': ['requests', 'json', 'jaraco.text','other_needed_packages'],
    'iconfile' : 'images/MyIcon.ico'
    'plist': {
        'CFBundleName': 'Tipply',
        'CFBundleDisplayName': 'Tipply',
        'CFBundleIdentifier': 'com.yourname.tipply',
        'CFBundleVersion': '0.1.0',
        'CFBundleShortVersionString': '0.1.0',
        'LSUIElement': False,
}

setup(
    include_package_data=True,
    name="Tipply",
    version="0.0.1",
    description="A simple way to send and receive digital tips",
    url="https://github.com/maglovskiNenad/hopplo",
    author="Maglovski Nenad",
    author_email="maglovskin@gmail.com",
    packages=setuptools.find_packages(),
    long_description="Tipply is a smart tool that simplifies tip distribution among employees based on CSV data. "
                     "Designed for managers, business owners, and team leads in the service industry, Tipply "
                     "automatically calculates how much tip each employee should receive — fairly, transparently,and"
                     " in just a few clicks.Simply upload a CSV file with employee work hours, roles, or earnings, and "
                     "Tipply takes care of the rest. The app uses customizable logic to divide tips proportionally, "
                     "ensuring everyone gets what they deserve. Say goodbye to manual spreadsheets, confusing "
                     "math, and disputes over fairness.Whether you're managing a restaurant, bar, hotel, or "
                     "any team that pools tips, Tipply helps you streamline payouts and keep things clear "
                     "and equitable.Tipply — because fair tip distribution shouldn’t be a guessing game.",
    long_description_content_type="text/markdown",
    app = APP,
    options={"py2app" : OPTIONS},
    setup_requires=["py2app","chardet","colorama","customtkinter","darkdetect","iniconfig","MouseInfo",
                    "numpy","packaging","pandas","pillow","pluggy","PyAutoGUI","PyGetWindow","Pygments",
                    "PyMsgBox","pyperclip","PyRect","PyScreeze","pytest","python-dateutil","pytweening",
                    "pytz","six","tabulate","tkinterdnd2","tzdata"
                    ],
    classifiers=[
        "Programing Language :: Python :: 3",
        "Operating System :: MacOS",
    ]
)
