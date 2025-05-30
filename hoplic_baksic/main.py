import pandas as pd
import customtkinter as ctk
from home_page import HomePage
from trinkgeld_actions import Trinkgeld_Actions

#Customtkinter classes
class App(ctk.CTk):
    def __init__(self,):
        super().__init__()
        self.title("\U0001F601")
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        window_width = int(screen_width * 0.6)
        window_height = int(screen_height * 0.6)

        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        #sidebar controller
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        #sidebar design
        self.sidebar_container = ctk.CTkFrame(self, corner_radius=10)
        self.sidebar_container.grid(row=0, column=0, sticky="ns", padx=20, pady=20)
        self.sidebar_container.grid_rowconfigure(0, weight=1)
        self.sidebar_container.grid_columnconfigure(0, weight=1)

        #sidebar
        self.sidebar = SidebarFrame(self.sidebar_container, self)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        #main poge design
        self.main_content = ctk.CTkFrame(self, corner_radius=10)
        self.main_content.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        self.main_content.grid_rowconfigure(0, weight=1)
        self.main_content.grid_columnconfigure(0, weight=1)

        #main page
        self.main_frame = MainFrame(self.main_content)
        self.main_frame.grid(row=0, column=0, sticky="ns")

        #home page
        self.show_home()

    def show_home(self):
        self.main_frame.show_page(HomePage)
    
    def show_trinkgeld_page(self):
        self.main_frame.show_page(Trinkgeld_Actions)

class SidebarFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, width=200)
        self.grid_rowconfigure(4, weight=1)

        #sidebar
        ctk.CTkLabel(self, text="App", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        ctk.CTkButton(self, text="Home", command=controller.show_home).pack(pady=10, padx=10)
        ctk.CTkButton(self,text="Trinkgeld",command=controller.show_trinkgeld_page).pack(pady=10, padx=10)

class MainFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.current_page = None
        
    def show_page(self, PageClass, **kwargs):
        if self.current_page:
            self.current_page.destroy()
        self.current_page = PageClass(self, **kwargs)
        self.current_page.pack(fill="both", expand=True)
        
if __name__ == "__main__":
    app = App()
    app.mainloop()