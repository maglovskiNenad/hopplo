# ===============================================================
# CSV reader
# Copyright (c) 2025 Maglovski Nenad
# This source code is licensed under the MIT
# license found in the LICENSE file.
# ===============================================================

import customtkinter as ctk

ctk.set_appearance_mode("Dark")

root = ctk.CTk()

root.withdraw()

SCREEN_WIDTH = root.winfo_screenwidth()
SCREEN_HEIGHT = root.winfo_screenheight()

WINDOW_WIDTH = int(SCREEN_WIDTH * 0.6)
WINDOW_HEIGHT = int(SCREEN_HEIGHT * 0.6)

