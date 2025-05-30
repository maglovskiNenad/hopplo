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
        ctk.CTkLabel(scrollable_frame, text="🧾 Welcome to the Tip & Work Hours Processing App",
                     font=title_font, anchor="center", justify="left").pack(anchor="center", padx=20, pady=(20, 10))

        # Features section
        ctk.CTkLabel(scrollable_frame, text="This application helps you:", font=section_font).pack(anchor="w", padx=20, pady=(5, 0))

        features = [
            "This application calculates individual tip distribution based on confirmed",
            "working hours per person and total daily tips.Data is read from two files:"
            "a CSV export with work hours and a tab-separated file with daily tips.",
            "After processing, the application provides a clear breakdown of tip allocation per worker.",
            "✅ Load a CSV file with employees’ working hours – auto-detect encoding & clean data.",
            "✅ Extract confirmed working hours per person and per date – ready for processing.",
            "✅ Import daily tip amounts – from a tab-delimited file with tips per time slot.",
            "✅ Automatically calculate how much tip each employee should receive – fair distribution.",
            "✅ Display totals per day and per person, including proportional tip distribution.",
        ]
        for line in features:
            ctk.CTkLabel(scrollable_frame, text=line, font=text_font).pack(anchor="w", padx=40, pady=1)

        # How it works section
        ctk.CTkLabel(scrollable_frame, text="\n🧠 How does it work?", font=section_font).pack(anchor="w", padx=20, pady=(10, 0))

        steps = [
            "1. Load the CSV file containing detailed working hours",
            "2. Load a CSV or TXT file containing daily tip amounts",
            "3. The app cleans and formats the data",
            "4. Filters confirmed work time entries",
            "5. Matches the data with tip amounts",
            "6. Calculates fair tip distribution per employee",
            "7. Shows a detailed table with: hours worked, tips received, and totals",
        ]
        for step in steps:
            ctk.CTkLabel(scrollable_frame, text=step, font=text_font).pack(anchor="w", padx=40, pady=1)

        # Powered by section
        ctk.CTkLabel(scrollable_frame, text="\n🛠 Powered by:", font=section_font).pack(anchor="w", padx=20, pady=(10, 0))

        techs = [
            "Pandas for data processing",
            "Chardet for automatic encoding detection",
            "CustomTkinter for a modern, intuitive user interface",
        ]
        for tech in techs:
            ctk.CTkLabel(scrollable_frame, text=f"- {tech}", font=text_font).pack(anchor="w", padx=40, pady=1)

        # Final note
        ctk.CTkLabel(scrollable_frame, text="\n💡 Navigate to the “Trinkgeld” section on the left to start!",
                     font=section_font).pack(anchor="w", padx=20, pady=(20, 10)) 
