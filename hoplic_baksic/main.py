import customtkinter as ctk
from home_page import HomePage
from trinkgeld_actions import TrinkgeldActions
from config import WINDOW_WIDTH,WINDOW_HEIGHT,SCREEN_WIDTH,SCREEN_HEIGHT

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("\U0001F601")

        x = int((SCREEN_WIDTH - WINDOW_WIDTH) / 2)
        y = int((SCREEN_HEIGHT - WINDOW_HEIGHT) / 2)

        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")

        #sidebar controller
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        #sidebar design
        self.sidebar_container = ctk.CTkFrame(self,corner_radius=0,fg_color="#2e2e2e")
        self.sidebar_container.grid(row=0, column=0, sticky="ns")
        self.sidebar_container.grid_rowconfigure(0, weight=1)
        self.sidebar_container.grid_columnconfigure(0, weight=1)

        #sidebar
        self.sidebar = SidebarFrame(self.sidebar_container, self)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        #main Page design
        self.main_content = ctk.CTkFrame(self,corner_radius=0,fg_color="#2e2e2e")
        self.main_content.grid(row=0, column=1, sticky="nswe")
        self.main_content.grid_rowconfigure(0, weight=1)
        self.main_content.grid_columnconfigure(0, weight=1)

        #main page
        self.main_frame = MainFrame(self.main_content)
        self.main_frame.grid(row=0, column=0)

        #home page
        self.show_home()

    def show_home(self):
        self.main_frame.show_page(HomePage)
    
    def show_trinkgeld_page(self):
        self.main_frame.show_page(TrinkgeldActions)

class SidebarFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, width=200)
        self.grid_rowconfigure(4, weight=1)

        self.actions = TrinkgeldActions(self)
        #sidebar
        ctk.CTkLabel(self, text="App", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        ctk.CTkButton(self, text="Home", command=controller.show_home).pack(pady=5, padx=5)
        ctk.CTkButton(self,text="Trinkgeld", command=controller.show_trinkgeld_page).pack(pady=5, padx=5)

class MainFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.current_page = None
        
    def show_page(self, page_class):
        if self.current_page:
            self.current_page.destroy()
        self.current_page = page_class(self)
        self.current_page.pack(fill="both", expand=True)
        
if __name__ == "__main__":
    app = App()
    app.mainloop()