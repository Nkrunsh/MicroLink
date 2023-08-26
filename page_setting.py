from tkinter import *
from tkinter import ttk
import pickle

class PageSettigs(Toplevel):
    """
    The PageSettigs class represents a settings page in the additional application's user interface of the main application. Contains methods to configure the relationships of the data received from serial communication with the execution of keyboard events.

    Attributes:

    -   parent: (Parent object) The parent object that the settings page belongs to.
    -   labels: (list) A list to hold the labels for the settings.
    -   entrys: (list) A list to hold the entry fields for the settings.
    -   settings: (dictionary) A dictionary to hold the key settings.

    Methods:

    -   __init__(self, parent): Initializes the settings page.
    -   get_settings_len(self) -> int: Returns the length of the settings.
    -   save_settings(self): Saves the settings to a file and updates the parent object with the new settings.
    """

    def __init__(self, parent):
        """Initializes the settings page."""

        super().__init__(parent)
        
        self.title("Keyboard Settings")
        self.configure(padx=20, pady=10)

        self.parent = parent
        self.labels:list = []
        self.entrys:list = []
        self.settings:dir = parent.key_Settings

        

        # UI construction 
        ttk.Label(self, text="Keyboard Settings", font=("Arial", 16)).grid(row=0, column=0,columnspan=4, pady=10, padx=60)
        
        # Settings Area
        for event in list(range(1,11)):
            label = ttk.Label(self,text=f"Message Received - {event}:")
            label.grid(row=event, column=1, padx=10, pady=5)
            self.labels.append(label)
            
            
            entry = ttk.Entry(self,justify='center', width=15)
            entry.insert(0,self.settings[event])
            entry.grid(row=event, column=2, padx=10, pady=5)
            
            self.entrys.append(entry)
        
        #Save botton
        ttk.Button(self,text="Save",width=50, command= self.save_settings).grid(row= 12, column=1, columnspan=2, padx=20, pady= 10)
    
    def get_settings_len(self) -> int: 
        """Returns the length of the settings."""

        return len(self.entrys) + 1

    def save_settings(self):
        """Saves the settings to a file and updates the parent object with the new settings."""

        # code save
        count_settings = self.get_settings_len()
        events = list(range(1,count_settings))

        for event, entry in zip(events, self.entrys):
            self.settings[event] = entry.get()

        self.parent.key_Settings = dict(self.settings)
        self.parent.rc.set_commands_event(self.settings)
        
        with open('microlinkdata.pkl', 'wb') as file:
            pickle.dump(self.parent.key_Settings, file)
  
        
        self.destroy()
