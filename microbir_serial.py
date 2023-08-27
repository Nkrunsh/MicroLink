import sys
import glob
import serial
import threading

from pynput.keyboard import Key, Controller

class MicrobitSerial:
    """
    This class represents a serial connection with a microbit to receive and send commands.

     Attributes:
    -   port (str) - The serial port to which the microbit is connected.
    -   baudrate (int) - The communication baud rate.
    -    timeout (int) - The timeout to receive data.
    -    state (bool) - The state of the serial connection.
    -    serial_thread - The thread of execution for serial communication.
    -    serial_socket (serial.Serial) - The serial connection object.
    -    commands_event (dict) - The dictionary of events and their associated commands.
    -    NO_PORT (str) - Default port if no valid port exists
    -    keyboard (Controller) - The keyboard event handler.
    
     Methods:
    -    set_port(port: str) -> None - Sets the serial port.
    -    set_baudrate(baudrate: int) -> None - Sets the baudrate of the communication.
    -    set_timeout(timeout: int) -> None - Sets the timeout.
    -    set_commands_event(commands: dict) - Sets the event commands.
    -    port_scan() -> list - Scans the available serial ports on the system.
    -    press(key: str) -> None - Simulates pressing a key on the keyboard.
    -    start_serial_communication() - Starts serial communication.
    -    stop_serial_communication() - Stops serial communication.
    -    _serial_worker() - Private method for the serial communication thread.
    -    _run_command(new_event: int) - Private method to execute the commands associated with the events.
    """

    def __init__(self, port:str = "--"):
        self.port = port            
        self.baudrate:int = 115200  
        self.timeout:int = 0.01     
        self.state:bool = False     
        self.serial_thread = None   
        self.serial_socket:serial.Serial = None
        self.commands_event:dict = None
        self.NO_PORT = "--"
        self.keyboard:Controller = Controller() 

    # -- SETTERS
    def set_port(self, port:str) -> None:
        """
        Sets the serial port.
        """
        self.port = port

    def set_baudrate(self,baudrate:int) -> None:
        """
        Sets the baudrate of the communication.
        """
        self.baudrate = baudrate
    
    def set_timeout(self, timeout:int) -> None:
        """
        Sets the timeout.
        """
        self.timeout = timeout

    def set_commands_event(self, commands:dict):
        """
        Sets the event commands.
        """
        self.commands_event = dict(commands)

    # -- UTILITY
    def port_scan(self) -> list:
        """ 
        Scans the available serial ports on the system.
        """
        
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass

        if len(result) == 0:
            result.append(self.NO_PORT)
            
        return result

    def press(self, key:str) -> None:
        """
        Simulates pressing a key on the keyboard.
        """

        self.keyboard.press(key)
        self.keyboard.release(key)
    
    # -- Serial comuni ation
    def start_serial_communication(self):
        """
        Starts serial communication.
        """

        if not self.state:
            self.state = True
            self.serial_thread = threading.Thread(target=self._serial_worker)
            self.serial_thread.start()

    def stop_serial_communication(self):
        """
        Stops serial communication.
        """

        self.state = False
        if self.serial_thread is not None:
            self.serial_thread.join()

    def _serial_worker(self):
        """
         Private method for the serial communication thread.
        """

        try:
            with serial.Serial(self.port, self.baudrate, timeout=self.timeout) as socket:
                while self.state:
                    if socket.in_waiting > 0:
                        try:
                            event = int(socket.readline().decode().strip())
                        except:
                            event = 0
                        self._run_command(event)
                                               
        except Exception as e:
            print("Thread error: ",e)

    def _run_command(self, new_event:int):
        """
        Private method for the serial communication thread.
        """
        
        for event, command in self.commands_event.items():
            if new_event == event:
                self.press(command)


    