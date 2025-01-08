import customtkinter as ctk
from .pages import MainPage, RegistirationPage

def def_logger(text: str):
    print(
        f"User GUI said: {text}"
    )

class GUI:
    def __init__(self):
        self.wn: ctk.CTk
        self.logger = def_logger
        self.wn: ctk.CTk = ctk.CTk()
        self.main_page: MainPage = MainPage(self.wn)
        self.regi_page: RegistirationPage = RegistirationPage(self.wn)
    
        self.e_name = self.regi_page.e_name
        self.e_record = self.main_page.e_record
        self.e_play = self.main_page.e_play

    def __init_wn(self):
        self.wn.title("New User")  
        self.wn.geometry("400x400")

    def __init_components(self):
        self.logger("components initializing")
        self.regi_page.create()
        self.main_page.create()

        self.regi_page.insert()
        self.main_page.insert()

        self.regi_page.pack(side='top', expand=True, fill='both')

    def switch_page(self):
        self.regi_page.pack_forget()
        self.main_page.pack(side='top', expand=True, fill='both')

    def init(self):
        self.__init_wn()
        self.__init_components()

    def run(self):
        self.logger("running ...")
        self.wn.mainloop()