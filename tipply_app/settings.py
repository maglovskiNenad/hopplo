# ===============================================================
# CSV reader
# Copyright (c) 2025 Maglovski Nenad
# This source code is licensed under the MIT
# license found in the LICENSE file.
# ===============================================================
from fnmatch import translate

import  customtkinter as ctk
from popup import Popup
from warning_msg import WarningPopup
from config import WINDOW_WIDTH,WINDOW_HEIGHT,title_font,text_font
import update

class SettingsActions(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)

        scrollable_frame = ctk.CTkScrollableFrame(self,width=WINDOW_WIDTH,height=WINDOW_HEIGHT)
        scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)

        #Title
        ctk.CTkLabel(
            scrollable_frame,
            text="Settings Page",
            font=title_font,
            anchor="center",
            justify="left"
        ).pack(anchor="center",padx=20, pady=(20, 10))

        row_frame_1 = ctk.CTkFrame(scrollable_frame)
        row_frame_1.pack(padx=20, pady=(10, 5), fill="x")

        ctk.CTkLabel(
            row_frame_1,
            text="The license is not difficult to find, a window will pop up right after you click on the 'License' button.",
            font=text_font,
            anchor="w",
            justify="left",
            wraplength=400,
        ).pack(side="left", padx=(0,10), fill="x", expand=True)

        ctk.CTkButton(row_frame_1,text="LICENSE",command=self.read_license,fg_color="transparent").pack(side="left")

        row2 = ctk.CTkFrame(scrollable_frame)
        row2.pack(padx=20, pady=(10, 5), fill="x")

        ctk.CTkLabel(
            row2,
            text="To check the update, click on 'UPDATE'",
            font=text_font,
            anchor="w",
            justify="left",
            wraplength=400
        ).pack(side="left", padx=(0, 10), fill="x", expand=True)

        ctk.CTkButton(
            row2,
            text="UPDATE",
            command=self.check_update,
            fg_color="transparent"
        ).pack(side="left")

    def read_license(self):
        try:
            with open("../LICENSE","r",encoding="utf-8")as file:
                text_license = file.read()
        except FileNotFoundError:
            WarningPopup(self,message="Not an existing file")

        Popup(self,message=text_license)

    def check_update(self):
        update.get_update()
