# ===============================================================
# CSV reader
# Copyright (c) 2025 Maglovski Nenad
# This source code is licensed under the MIT
# license found in the LICENSE file.
# ===============================================================

import customtkinter as ctk
from config import WINDOW_WIDTH,WINDOW_HEIGHT


class Popup(ctk.CTkToplevel):
    def __init__(self,parent,message="Message to you"):
        super().__init__(parent)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.grab_set()

        scrollable_frame = ctk.CTkScrollableFrame(self, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)

        label = ctk.CTkLabel(
            scrollable_frame,
            text=message,
            wraplength=WINDOW_WIDTH,
            font=("Segoe UI", 26, "italic"),
            text_color="#1e90ff",
            justify="left"
        )

        label.pack(pady=(25, 15), padx=10)

        ctk.CTkButton(self, text="Ok", command=self.destroy).pack(pady=10)
