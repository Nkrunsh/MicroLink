import pickle
import os.path

from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk

from page_setting import PageSettigs
from microbir_serial import MicrobitSerial

class HomePage(ttk.Frame):

    """
    HomePage is a class that represents the main UI application

    Attributes:
        -   rc: MicrobitSerial Object: Represents the serial communication with the Micro:bit board.
        -   parent: ThemedTk: Represents the main window of the application.
        -   key_Settings: Dict: Stores key and event settings.
        -   DEFAULT_KEY: Dict: Stores a dictionary with the default keys.
        -   portvar: StringVar: Stores the variable of the selected port.
        -   serial_thread: Thread: Serial communication thread.
        -   portSelector: Combobox: Serial port selector.
        -   baudratevar: IntVar: Stores the selected baud rate variable.
        -   connectBtn: Button: Allows you to control the serial connection.
        -   ttk.Label, ttk.Button: They are used to create the user interface.
            
        Methods:
        -   open_settings (): Open the settings page
        -   serial_control (): Control the serial connection
        -   refresh_prot (TkinterEvent) : Refresh the port list
        -   load_settings () :Load event and key configuration from a document
        -   kill () : Allows to end the serial communication thread
    """


    def __init__(self, parent:ThemedTk, container:Frame):
        """
        Initialize the home page
        
        Args:
            -   parent (ThemedTk): The parent window
            -   container (Frame): The container frame

        """
        super().__init__(container)
        
        self.rc:MicrobitSerial = MicrobitSerial()
        self.parent = parent
        self.key_Settings:dict = {}
        self.DEFAULT_KEY:dict = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i', 10: 'j'}

        portList:list = self.rc.port_scan()
        self.portvar = StringVar(value=str(portList[0]))
        self.load_settings()
        self.serial_thread = None

        # UI construction 
        self.main_frame = ttk.Frame(self)
        self.main_frame.config(border=5)
        self.main_frame.pack(anchor=CENTER,side=TOP, padx=30, pady=5)
        


        # SERIAL PORT 
        ttk.Label(self.main_frame, text="Serial Port ").grid(row=0,column=0, padx=0, pady=15)
        self.portSelector = ttk.Combobox(self.main_frame,textvariable=self.portvar,width=8, values=portList,state="readonly" )
        self.portSelector.bind("<Enter>",self.refresh_port)
        self.portSelector.grid(row=0,column=2)

        #BAUDRATE
        ttk.Label(self.main_frame, text="Baudrate").grid(row=0, column=3, padx=0, pady=0)
        baudrateList = [9600, 14400, 19200, 38400, 57600, 115200]
        self.baudratevar = IntVar(value=baudrateList[-1])
        ttk.Combobox(self.main_frame, width=8, state="readonly",
                    textvariable=self.baudratevar, values=baudrateList).grid(row=0,column=4)

        # SETTIGNS
        ttk.Button(self.main_frame,text= "Keyboard Actions", width=25,command=self.open_settings).grid(row=1, column=0, columnspan=3, padx=10, pady=0)

        #SERIAL CONECTION
        self.connectBtn = ttk.Button(self.main_frame,text= "Connect", width=25,command=self.serial_control)
        self.connectBtn.grid(row=1, column=3, columnspan=3, pady=0, padx= 10)  

        #LOG BAR
        self.logbar = ttk.Label(self, text="Welcome to Micro:Link. Connect your device to get started", anchor=W)   
        self.logbar.pack(side=BOTTOM, fill=X,padx=10,ipady=3)
    
    def open_settings(self) -> None:
        """Open the settings page"""

        PageSettigs(self)
        
    def serial_control(self) -> None:
        """Control the serial connection"""

        if self.rc.state:   #Cambia Conectado -> Desconectado
            
            self.rc.state =False
            self.connectBtn.configure(text="Connect")
            if self.rc.stop_serial_communication():
                self.logbar.config(text="Port disconnected successfully")
            

            
        else:               #Cambia Desconectado -> Conectado
            if self.portvar.get() != self.rc.NO_PORT:
                self.rc.set_port(self.portvar.get())
                self.rc.set_baudrate(self.baudratevar.get())
                self.rc.start_serial_communication()   
                self.rc.set_commands_event(self.key_Settings)
                self.connectBtn.configure(text="Dissconect")
                self.logbar.config(text="Port connected successfully")
            else:
                self.logbar.config(text="Invalid port, check before connecting")

            

        
    def refresh_port(self, event) -> None: 
        """Refresh the port list"""

        self.portSelector['values'] = self.rc.port_scan()

    def load_settings(self)-> None:
        """Load event and key configuration from a document"""

        if os.path.isfile('microlinkdata.pkl'):
            with open('microlinkdata.pkl', 'rb') as file:
                self.key_Settings = pickle.load(file)
        else:
            with open('microlinkdata.pkl', 'wb') as file:
                pickle.dump(self.DEFAULT_KEY, file)
            self.key_Settings = dict(self.DEFAULT_KEY)

    def kill(self):
        """Allows to end the serial communication thread"""

        self.rc.stop_serial_communication()