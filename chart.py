import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
import numpy as np


def setup(self):
    """ Set up matplotlib plotting canvas and layout. """
    self.curves = [i for i in range(self.params_num)]
    self.f = Figure(figsize=(6,5), dpi=100)
    self.axis1 = self.f.add_subplot(111)
    self.axis2 = self.axis1.twinx()  # create a second y-axis
    # self.axis1.set_xlim([0, 200]);
    # self.axis1.set_ylim([0, 200]);
    ax_plot(self, self.plotdata)
    self.canvas = FigureCanvasTkAgg(self.f, self)
    self.canvas.get_tk_widget().pack(anchor='w', fill=BOTH, expand=YES)
    self.canvas.get_tk_widget().place(x=5, y=25)
    self.canvas._tkcanvas.pack(anchor='w', fill=BOTH, expand=YES)
    self.canvas._tkcanvas.place(x=5, y=25)
    self.f.tight_layout() # otherwise the right y-label is slightly clipped




def ax_plot(self, data):
    """ 
    Plot the axes and values. This method is called when first creating the plot.
    For plot updates, call set_plot(...)
    Detect whether checkboxes are checked, and display corresponding output curve accordingly.
    """
    # PRIMARY Y-AXIS
    for i in range(self.params_num):
        param_name = self.params.get(i)
        if i != 0: # Exclude because i=0 is plotted on the secondary y-axis
            if self.checkboxes_checked[i].get() == 1:
                self.curves[i], = self.axis1.plot(
                                                data.get("time"), 
                                                data.get(param_name), 
                                                color=self.legend.get(param_name), 
                                                linewidth=1, 
                                                alpha=0.7)
    self.axis1.set_xlabel('Time (s)')
    self.axis1.set_ylabel('Temperature (\u00B0C)')

    # SECONDARY Y-AXIS
    if self.checkboxes_checked[0].get() == 1:
        self.curves[0], = self.axis2.plot(
                                        data.get("time"),
                                        data.get("p1"), 
                                        color=self.legend.get("p1"), 
                                        linewidth=1, 
                                        alpha=0.7)
    self.axis2.tick_params(axis='y', labelcolor='b')
    self.axis2.set_ylabel('Pressure (psig)', color='b')  # we already handled the x-label with ax1




def set_plot(self, data):
    """
    Updates the existing plot. 
    Detect whether checkboxes are checked, and display corresponding param curve accordingly.
    """
    try:
        visible = set()
        for i in range(self.params_num):
            if i != 0: # Exclude because i=0 is plotted on the second y-axis
                param_name = self.params.get(i)
                if self.checkboxes_checked[i].get() == 1:
                    self.curves[i].set_xdata(data.get("time"))
                    self.curves[i].set_ydata(data.get(param_name))
                    visible.add(param_name)

        # Get axis min/max values
        x_min, x_max = get_minmax(data.get("time"))
        y2_min, y2_max = get_minmax(data.get("p1")) # Second y-axis
        try:
            # for all curves plotted on y-axis. Find the minimum of all minima, and maximum of all maxima.
            y_min = fix_axis_minmax(min([min(val_list) for key,val_list in data.items() if key in visible]))
            y_max = fix_axis_minmax(max([max(val_list) for key,val_list in data.items() if key in visible])) 
        except:
            y_min, y_max = 0,0

        # If checkbox on, then plot the curve for that param
        if self.checkboxes_checked[0].get() == 1:
            self.curves[0].set_xdata(data.get("time"))
            self.curves[0].set_ydata(data.get("p1"))

        # # Set axis ranges with some padding
        self.axis1.set_xlim([x_min, x_max*1.05])
        self.axis1.set_ylim([y_min*0.95, y_max*1.05])
        self.axis2.set_ylim([y2_min*0.95, y2_max*1.05]) # Second y-axis
        self.canvas.draw()
    except Exception as e:
        print("Exception in set_plot().", e)



def get_minmax(datalist):
    """
    None element throws an error, but np.nan does not.
    Exception thrown when np.nan is only element in the list. In this case, return 0,0.
    """
    return fix_axis_minmax(min(datalist)), fix_axis_minmax(max(datalist))

def fix_axis_minmax(val):
    """ Axis min/max cannot be None or np.NaN. Change these to 0. """ 
    return 0 if val is None or np.isnan(val) else val


def update_plot(self):
    self.axis1.cla()
    self.axis2.cla()
    ax_plot(self, self.plotdata)   
    self.canvas.draw() #self.update()


# def resize_axes(self):
#     self.axis1.set_xlim([0,1])
#     self.axis1.set_ylim([0,1])
#     self.axis2.set_ylim([0,1])
