# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path


project_root = Path(SPECPATH).resolve()
app_dir = project_root / "tipply_app"
icon_path = app_dir / "images" / "MyIcon.ico"

datas = [
    (str(project_root / "LICENSE"), "."),
    (str(app_dir / "version.txt"), "."),
    (str(app_dir / "images"), "images"),
]

hiddenimports = [
    "tkinterdnd2",
    "PIL",
    "pyautogui",
]


a = Analysis(
    [str(app_dir / "main.py")],
    pathex=[str(app_dir)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="hopplo",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon=str(icon_path),
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="hopplo",
)
