import numpy as np
import sys
import glob
import serial # install as: pip install pyserial
import time
import math
import minimalmodbus



def serial_ports():
    """ 
    Lists serial port names
    Raises EnvironmentError:
            Unsupported or unknown platforms
    Returns:
            A list of the serial ports available on the system
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
    return result




def serial_setup(port, baudrate, timeout):
    """
    Set up serial connection with controller
    timeout of 0 makes readline "non-blocking"
    if timeout is 0.01, not all bits read, and erroneous values henceforth derived.
    """
    print(f"Reading port: {port}")
    return serial.Serial(port=port, baudrate=baudrate, timeout=timeout)




"""
===================================================================
DUMMY CONTROLLER FOR TESTING
===================================================================
The outputs are simulated using arbitrary functions, where x is
generated using a counter.
"""
class Dummy:

    def __init__(self, com_port, baudrate, timeout):
        # The arguments are not relevant for the Dummy controller, 
        # but are necessary for real controllers with a serial connection.
        self.com_port = com_port
        self.baudrate = baudrate
        self.timeout = timeout
        self.activate()


    def activate(self):
        
        # Create a counter to provide x to the simulating functions.
        # Calling self.counter() will increase its count by 1 each time.
        def create_counter():
            count = 0
            def increase_count():
                nonlocal count
                count += 1
                return count
            return increase_count
        self.counter = create_counter()


    def read(self):
        """
        Return a dictionary of output readings for each parameter.
        """
        try:      
            time.sleep(0.05)     
            x = self.counter()
            # Arbitrary functions to simulate sensor outputs
            nums = [1,1,1,2,None,4,5,6,5,4,7,8,9,7,8,9,10,11,9,9,8,7,8,9,10]
            val1 = nums[x % len(nums)]      
            val2 = (12*x)/(1 + 0.5*x) + 1   
            val3 = (0.5*x)/(1 + 0.04*x)   
            val4 = 5/(1 + math.exp(-0.1*x))   
            val5 = np.nan
            readings = [val1, val2, val3, val4, val5]

            # Round the floats and handle all bad values as np.nan
            for i, reading in enumerate(readings):
                try:
                    readings[i] = round(reading,2) 
                except Exception as e:
                    readings[i] = np.nan 

            return {
                "p1": readings[0],
                "t1": readings[1],
                "t2": readings[2],
                "t3": readings[3],
                "t4": readings[4],
            }

        except Exception as e:
            print("Exception:", e)
            return {
                "p1": np.nan,
                "t1": np.nan,
                "t2": np.nan,
                "t3": np.nan,
                "t4": np.nan
            }


    def write(self, to_send):
        pass 

    def change_setpoint(self):
        pass

    def reset(self):
        self.activate()

    def shutdown(self):
        pass





