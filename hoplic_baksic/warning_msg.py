# ===============================================================
# CSV reader
# Copyright (c) 2025 Maglovski Nenad
# This source code is licensed under the MIT
# license found in the LICENSE file.
# ===============================================================

import customtkinter as ctk

class WarningPopup(ctk.CTkToplevel):
    def __init__(self,parent,title="Oooops...",message="Message to you"):
        super().__init__(parent)
        self.title(title)
        self.geometry("300x150")
        self.grab_set()

        ctk.CTkLabel(self, text=message, wraplength=280).pack(pady=(20, 10))
        ctk.CTkButton(self, text="Ok", command=self.destroy).pack(pady=10)
