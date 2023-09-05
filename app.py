from tkinter import *
from ttkthemes import ThemedTk
from home_page import HomePage

class App(ThemedTk):
    """
    App is a class that represents the main application.

    Attributes:
        None

    Methods:
        __init__(): Initializes the App instance.
        show_frame(): Shows a specific frame.
        on_closing(): Handles the closing event of the application.
    """
    def __init__(self):
        """
        Initializes the App instance.
        """
        super().__init__(theme="breeze")

        self.title("Micro:Link")
        self.resizable(False, False)
        self.iconphoto(False, PhotoImage(file="resources/usb.png"))
        #<a href="https://www.flaticon.es/iconos-gratis/usb" title="usb iconos">Usb iconos creados por srip - Flaticon</a>
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        container = Frame(self, bg="#d8ebff")
        container.pack(side="top", fill="both", expand=True, padx=0, pady=0)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frame = HomePage(self, container)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.tkraise()
        
    def on_closing(self):
        """
        Handles the closing event of the application.
        """
        self.frame.kill()
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()