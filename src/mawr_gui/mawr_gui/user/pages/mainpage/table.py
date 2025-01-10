import customtkinter as ctk

from mguitb import IComponent
from mguitb import TableData
from mguitb import Table as TableWidget


class TNavigator(IComponent):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.received_btn: ctk.CTkButton
        self.recorded_btn: ctk.CTkButton
        self.sended_btn: ctk.CTkButton

    def create(self):
        self.received_btn = ctk.CTkButton(self, text="received")
        self.recorded_btn = ctk.CTkButton(self, text="recorded")
        self.sended_btn = ctk.CTkButton(self, text="sended")
        return super().create()

    def insert(self):
        self.received_btn.grid(row=0, column=0)
        self.recorded_btn.grid(row=0, column=1)
        self.sended_btn.grid(row=0, column=2)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        return super().insert()



class ETableFaces:
    RECEIVED: int = 0 
    RECORDED: int = 1
    SENDED: int = 2



class Table(IComponent):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.table_datas: tuple[TableData] = (
            TableData(), TableData(), TableData()
        )
        self.__table_face: int = ETableFaces.RECEIVED
        
        self.navigator: TNavigator = TNavigator(self)
        self.table_widget: TableWidget

    def config_table_data(self, face_no: int = None, cols = None, rows = None):
        face_no = face_no if face_no else self.__table_face
        
        if cols is not None: self.table_datas[face_no].cols = cols
        if rows is not None: self.table_datas[face_no].rows = cols

        if face_no == self.__table_face: self.table_widget.refresh_data()

    def create(self):        
        self.navigator.create()
        self.table_widget = TableWidget(self)
        self.table_widget.refresh_data(
            self.table_datas[self.__table_face]
        )
        return super().create()
    
    def insert(self):
        self.navigator.insert()
        self.navigator.grid(row=0, column=0, sticky='nswe')
        self.table_widget.grid(row=0, column=1, sticky='nswe')
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=10)
        return super().insert()
    
    