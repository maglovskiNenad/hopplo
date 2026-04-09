# ===============================================================
# CSV reader
# Copyright (c) 2025 Maglovski Nenad
# This source code is licensed under the MIT
# license found in the LICENSE file.
# ===============================================================
import platform
import webbrowser
from requests import get
from tkinter import messagebox
from paths import resource_path

GITHUB_REPO = "maglovskiNenad/hopplo"

def get_local_version():
    with open(resource_path("version.txt"), "r", encoding="utf-8") as f:
        return  f.read().strip()

def get_latest_release():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
    response = get(url)
    if response.status_code != 200:
        raise  Exception("No update available!")
    return response.json()

def get_download_url(release_data):
    assets = release_data.get("assets", [])
    if not assets:
        return release_data["html_url"]

    system_name = platform.system().lower()
    machine = platform.machine().lower()

    preferred_markers = {
        "windows": ["windows", "win"],
        "darwin": ["macos", "mac", "osx"],
        "linux": ["linux"],
    }
    arch_markers = {
        "arm64": ["arm64", "aarch64"],
        "aarch64": ["arm64", "aarch64"],
        "x86_64": ["x64", "x86_64", "amd64"],
        "amd64": ["x64", "x86_64", "amd64"],
    }

    system_markers = preferred_markers.get(system_name, [system_name])
    machine_markers = arch_markers.get(machine, [machine])

    for asset in assets:
        name = asset["name"].lower()
        if any(marker in name for marker in system_markers) and any(marker in name for marker in machine_markers):
            return asset["browser_download_url"]

    for asset in assets:
        name = asset["name"].lower()
        if any(marker in name for marker in system_markers):
            return asset["browser_download_url"]

    return assets[0]["browser_download_url"]

def get_update():
    local_version = get_local_version()
    try:
        release_data = get_latest_release()
    except Exception as e:
        messagebox.showerror("Error",str(e))
        return

    latest_version = release_data["tag_name"].lstrip("v")
    download_url = get_download_url(release_data)

    if local_version == latest_version:
        messagebox.showinfo("Update", f"App is already up to date ({local_version})")
        return

    answer = messagebox.askyesno(
        "Update available",
        f"A new version of {latest_version} is available.\nCurrent: {local_version}\n\nDo you want to open the download page?"
    )

    if answer:
        try:
            webbrowser.open(download_url)
        except Exception as e:
            messagebox.showerror("Update error", str(e))
