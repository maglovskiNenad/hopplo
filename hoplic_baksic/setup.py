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
    "iconfile" : "images/MyIcon.ico"
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
    long_description="",
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