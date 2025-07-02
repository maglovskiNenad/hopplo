# ===============================================================
# CSV reader
# Copyright (c) 2025 Maglovski Nenad
# This source code is licensed under the MIT
# license found in the LICENSE file.
# ===============================================================

import pandas as pd
import customtkinter as ctk


class HomePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        window_width = int(screen_width * 0.6)
        window_height = int(screen_height * 0.6)

        # Scrollable frame container
        scrollable_frame = ctk.CTkScrollableFrame(self, width=window_width, height=window_height)
        scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Fonts
        title_font = ctk.CTkFont(size=20, weight="bold")
        section_font = ctk.CTkFont(size=14, weight="bold")
        text_font = ctk.CTkFont(size=12)

        # Title
        ctk.CTkLabel(
            scrollable_frame,
            text="🧾 Welcome to the Tip & Work Hours Processing App",
            font=title_font,
            anchor="center",
            justify="left"
        ).pack(anchor="center", padx=20, pady=(20, 10))

        # Features introduction
        ctk.CTkLabel(
            scrollable_frame,
            text="This application helps you streamline the calculation of employee tips based on actual working hours.",
            font=text_font,
            wraplength=window_width - 40,
            justify="left"
        ).pack(anchor="w", padx=20, pady=(5, 15))

        # Features section
        ctk.CTkLabel(scrollable_frame, text="🔍 Key Features:", font=section_font).pack(anchor="w", padx=20, pady=(5, 5))

        features = [
            "✅ Automatically read and clean exported CSV files with employees’ working hours.",
            "✅ Detects and handles different file encodings using the Chardet library.",
            "✅ Supports drag-and-drop interface for intuitive file uploads.",
            "✅ Extracts only confirmed work hours (‘Bestätigte Arbeitszeit’) for accurate calculations.",
            "✅ Loads daily tip amounts from a separate tab-separated file.",
            "✅ Matches each employee’s working hours with the relevant day’s tip amount.",
            "✅ Calculates fair tip distribution proportionally, based on hours worked.",
            "✅ Presents the final results in a clean, formatted table inside the app.",
        ]
        for line in features:
            ctk.CTkLabel(scrollable_frame, text=line, font=text_font, wraplength=window_width - 60).pack(anchor="w",
                                                                                                         padx=40,
                                                                                                         pady=2)

        # How it works section
        ctk.CTkLabel(scrollable_frame, text="\n🧠 How does it work?", font=section_font).pack(anchor="w", padx=20,
                                                                                             pady=(20, 5))

        steps = [
            "1. Open the 'Trinkgeld' section from the sidebar.",
            "2. Drag and drop two files into the drop zone: one with working hours and one with tips.",
            "3. The app will validate the file contents and clean up inconsistent data.",
            "4. It filters only confirmed working time entries relevant to tip calculations.",
            "5. Then it matches these entries with the daily tips for each time slot.",
            "6. The tip distribution is calculated by dividing total tips per hour, then multiplying by hours per employee.",
            "7. The results are displayed in a scrollable table with totals per person and per day.",
        ]
        for step in steps:
            ctk.CTkLabel(scrollable_frame, text=step, font=text_font, wraplength=window_width - 60).pack(anchor="w",
                                                                                                         padx=40,
                                                                                                         pady=2)

        # Use cases
        ctk.CTkLabel(scrollable_frame, text="\n🎯 Who is this for?", font=section_font).pack(anchor="w", padx=20,
                                                                                            pady=(20, 5))

        audience = [
            "✔️ Café or bar managers who manage part-time staff with tip-based compensation.",
            "✔️ Teams that split tips fairly and want transparency in the calculation.",
            "✔️ Anyone who needs to merge shift logs and financial data quickly and reliably.",
        ]
        for item in audience:
            ctk.CTkLabel(scrollable_frame, text=item, font=text_font).pack(anchor="w", padx=40, pady=1)

        # Powered by section
        ctk.CTkLabel(scrollable_frame, text="\n🛠 Powered by:", font=section_font).pack(anchor="w", padx=20,
                                                                                       pady=(20, 5))

        techs = [
            "📊 Pandas – high-performance data analysis and manipulation.",
            "🔍 Chardet – smart encoding detection for reading international data files.",
            "🎨 CustomTkinter – modern-looking Python GUI framework with great flexibility.",
        ]
        for tech in techs:
            ctk.CTkLabel(scrollable_frame, text=tech, font=text_font).pack(anchor="w", padx=40, pady=1)

        # Final instruction
        ctk.CTkLabel(
            scrollable_frame,
            text="\n💡 Ready to get started? Use the sidebar and head over to the 'Trinkgeld' section to begin your calculations!",
            font=section_font,
            wraplength=window_width - 40
        ).pack(anchor="w", padx=20, pady=(30, 20))
