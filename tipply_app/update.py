# ===============================================================
# CSV reader
# Copyright (c) 2025 Maglovski Nenad
# This source code is licensed under the MIT
# license found in the LICENSE file.
# ===============================================================
from pyexpat.errors import messages
from requests import get, status_codes
import subprocess
import os
import sys
import tempfile
import customtkinter as ctk
from tkinter import messagebox
from warning_msg import WarningPopup
from popup import Popup

GITHUB_REPO = "maglovskiNenad/hopplo"
LOCALE_VERSION_FILE = "../version.txt"

def get_local_version():
    with open(LOCALE_VERSION_FILE, "r")as f:
        return  f.read().strip()

def get_last_version():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/late"
    response = get(url)
    if status_codes != 200:
        raise  Exception("No update available!")
    data = response.json()
    return data["tag_name"].lstrip("v"),data["assets"][0]["browser_download_url"]

def download_dmg(url):
    print(f"Downloading:{url}")
    r = get(url, stream=True)
    if r.status_code != 200:
        raise Exception("Download failed")
    temp_dmg = os.path.join(tempfile.gettempdir(), "update.dmg")
    with open(temp_dmg, "wb") as f:
        for chunk in r.iter_content(1024*1024):
            f.write(chunk)
    return temp_dmg

def mount_and_install(dmg_path):
    subprocess.run(["hdiutil", "attach", dmg_path])
    messagebox.showinfo("Update", "The new version is mounted. Open a window and drag the application to /Applications.")

def get_update():
    local_version = get_last_version()
    try:
        latest_version,dmg_url = get_last_version()
    except Exception as e:
        messagebox.showerror("Error",str(e))
        return

    if local_version == latest_version:
        messagebox.showinfo("Update", f"App is already up to date ({local_version})")

    answer = messagebox.askyesno(
        "Update available",
        f"A new version of {latest_version} is available.\nCurrent: {local_version}\n\nDo you want to download it?"
    )

    if answer:
        try:
            dmg_path = download_dmg(dmg_url)
            mount_and_install(dmg_path)
        except Exception as e:
            messagebox.showerror("Update error", str(e))