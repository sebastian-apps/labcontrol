"""
===========
LABCONTROL
===========
Created by Sebastian Sessarego


LabControl is designed to monitor and control your process equipment in a laboratory or plant. 
Consolidate all your sensor and controller output data and plot the data real-time for monitoring processes. 
Temperature, pressure, mass, voltage, and any other reading from your process equipment can be integrated into LabControl.
Data can also be exported for future data analysis.

The software is currently set up to read from a pressure transducer and four thermocouples.
However, the software can be easily modified to suit your needs. Tkinter is used for the Python GUI. Plotting is performed using matplotlib. 

Future version will include options to write to the controller.
"""

from tkinter import *
import tkinter as tk
import datetime
import matplotlib
matplotlib.use("TkAgg")

# LabControl modules
import widgets
import chart
import controllers
import exportfile


SAMPLING_RATE = 500   
DEBUG = True


class Window(Frame):
    """
    This constitutes the main window that plots all readings over time.
    """

    def init_plotdata(self): 
        return {
            "time": [],
            "p1": [],
            "t1": [],
            "t2": [],
            "t3": [],
            "t4": [],
        }


    def __init__(self, master=None, com_port=None):
        # Init the Tkinter Window
        Frame.__init__(self, master)
        self.master = master
        self.master.title("LabControl")
        self.pack(fill=BOTH, expand=1)

        # Start the controller
        # The Dummy controller is used for testing purposes.
        self.controller = controllers.Dummy(com_port=com_port, baudrate=9600, timeout=2)

        # Initialize 
        self.params = {
                    0: "p1",
                    1: "t1",
                    2: "t2",
                    3: "t3",
                    4: "t4"
        }
        self.legend = {
                    "p1": "#0000ff",
                    "t1": "#ff0000",
                    "t2": "#ff6200",
                    "t3": "#8b4513",
                    "t4": "#000"
                }
        self.params_num = len(self.params) # Number of params to be plotted against x-axis (time) and will also have a checkbox.
        self.plotdata = self.init_plotdata()
        self.filesaved = ""
        self.start_time = datetime.datetime.now()
        self.time = 0
        self.message_timer = 0

        # Build Widgets
        widgets.build_buttons(self)
        widgets.build_output_labels(self)
        widgets.build_checkboxes(self)
        widgets.build_message(self)
        # Set up the plot
        chart.setup(self)




    def clock(self):

        # Get time and most current readings from controllers
        self.time = self.get_time_elapsed()
        readings = self.controller.read()

        # Update the message timer
        self.message_timer -= 1
        if self.message_timer == 0:
            self.show_message("")

        # Update label widgets with readings
        widgets.output_reading(self.label_time, self.time)
        for param, reading in self.labels.items():
            widgets.output_reading(self.labels[param], readings[param])

        # Update the plot
        try:         
            self.plotdata["time"].append(self.time) 
            for param, reading in readings.items():
                self.plotdata[param].append(reading)    
            chart.set_plot(self, self.plotdata) # self.update_plot() is an expensive alternative
        except Exception as e:
            self.show_message("Error in reading data!")
            print(e)

        self.master.after(SAMPLING_RATE, self.clock)


    def get_time_elapsed(self):
        """ Return number of seconds of time elapsed """
        return int(round((datetime.datetime.now() - self.start_time).total_seconds(),0))



    def reset(self):
        """ Reset. Clear the plot. Previous values will be lost. """
        self.plotdata = self.init_plotdata()
        self.time = 0
        self.start_time = datetime.datetime.now()
        chart.update_plot(self)


    def saveas(self):
        exportfile.saveas(self)

    def save(self):
        exportfile.save(self)

    def exit(self):
        """ Exit the application. """
        self.controller.shutdown()
        self.master.destroy()







class FirstWindow:
    """
    The first windows determines if communication devices are connected. Without connected devices, the software 
    cannot proceed to reading and plotting, unless in Debug mode. 
    """
    def __init__(self, master):
        self.master = master
        self.master.title("LabControl")
        self.frame = Frame(self.master)  
        self.frame.pack(fill=X)

        # Initialize
        self.found_devices = []
        self.om_variable = StringVar()
        self.com_port = None

        # Set up the GUI widgets
        self.textbox = Label(self.frame, text="LabControl", height=2)
        self.textbox.config(font=("Arial", 25), fg="#000", background="#fff")
        self.textbox.pack(fill=X, expand=True)

        self.textbox = Label(self.frame, height=2, bg='light gray')
        self.textbox.config(font=("Arial", 10), fg="#fff", background="#000")
        self.textbox.pack(fill=X, expand=True)

        # Look for connected devices
        self.found_devices = controllers.serial_ports()
        if self.found_devices:
            self.om_variable.set(self.found_devices[0])
            self.com_port = self.found_devices[0]

        # Display a dropdown menu of available devices
        self.DevicesMenu = OptionMenu(self.frame, self.om_variable, self.found_devices, command=self.options_callback)
        self.DevicesMenu.pack(pady=10)

        # Additional GUI
        self.FindDevicesButton = Button(self.frame, text='Find Devices', width=25, command=self.find_devices) 
        self.FindDevicesButton.pack(pady=10)

        self.StartButton = Button(self.frame, fg="#fff", bg="#0000ff", text='Start', width=25, command=self.new_window) 
        self.StartButton.pack(pady=10)
        # self.find_devices()


    def find_devices(self):
        """ Look for devices connected to COM ports. """
        print("find devices...")
        self.found_devices = controllers.serial_ports()
        menu = self.DevicesMenu["menu"]
        menu.delete(0, "end")
        for string in self.found_devices:
            menu.add_command(label=string,
                             command= tk._setit(self.om_variable, string, self.options_callback))

        if len(self.found_devices) == 0:
            self.com_port = None
            self.textbox.config(text="Devices not found. Please connect devices and press 'Find Devices'.")
            if DEBUG: # Don't need devices connected in Debug mode
                self.StartButton.configure(state="normal", bg="#0000ff")
            else:
                self.StartButton.configure(state="disabled", bg='light gray')   
            
        else:
            self.com_port = self.found_devices[0]
            self.textbox.config(text=f"Devices found. Reading Port {self.com_port}.")
            self.StartButton.configure(state="normal", bg="#0000ff")


    def options_callback(self, selection):
        self.com_port = selection
        self.textbox.config(text=f"Reading Port {self.com_port}.")


    def close_windows(self):
        self.master.destroy()
        self.new_window
    def new_window(self):
        self.master.destroy() # close the current window
        self.master = tk.Tk() # create another Tk instance
        self.master.geometry("1100x550")
        self.master.resizable(False, False)
        self.app = Window(self.master, self.com_port) # proceed to main window: Window
        self.master.after(1000, self.app.clock)
        self.master.mainloop()



def main():
    root = Tk()
    root.geometry("700x400")
    app = FirstWindow(root)
    root.resizable(False, False)
    root.mainloop()




if __name__ == "__main__":
    main()
