import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
import numpy as np


def setup(ctx):
    """ Set up matplotlib plotting canvas and layout. """
    ctx.curves = {param: None for param in ctx.config.get("params")}
    ctx.f = Figure(figsize=(6,5), dpi=100)
    ctx.axis1 = ctx.f.add_subplot(111)
    ctx.axis2 = ctx.axis1.twinx()  # create a second y-axis
    # ctx.axis1.set_xlim([0, 200]);
    # ctx.axis1.set_ylim([0, 200]);
    start_plot(ctx, ctx.plotdata)
    ctx.canvas = FigureCanvasTkAgg(ctx.f, ctx)
    ctx.canvas.get_tk_widget().pack(anchor='w', fill=BOTH, expand=YES)
    ctx.canvas.get_tk_widget().place(x=5, y=25)
    ctx.canvas._tkcanvas.pack(anchor='w', fill=BOTH, expand=YES)
    ctx.canvas._tkcanvas.place(x=5, y=25)
    ctx.f.tight_layout() # otherwise the right y-label is slightly clipped




def start_plot(ctx, data):
    """ 
    Plot the axes and values. This method is called when first creating the plot.
    For plot updates, call set_plot(...)
    Detect whether checkboxes are checked, and display corresponding output curve accordingly.
    """

    for param_name, specs in ctx.config.get("params").items():
        if ctx.checkboxes_checked[param_name].get() == 1:
            if specs.get("axis") == "y1":   # primary y-axis          
                ctx.curves[param_name], = ctx.axis1.plot(
                                                data.get("time"), 
                                                data.get(param_name), 
                                                color=ctx.legend.get(param_name), 
                                                linewidth=1, 
                                                alpha=0.7)
            elif specs.get("axis") == "y2":   # secondary y-axis  
                ctx.curves[param_name], = ctx.axis2.plot(
                                                data.get("time"),
                                                data.get(param_name), 
                                                color=ctx.legend.get(param_name), 
                                                linewidth=1, 
                                                alpha=0.7)

    # Set axes labels and colors
    axes = ctx.config.get("axes")
    ctx.axis1.set_xlabel(axes.get("x").get("label"), color=axes.get("x").get("color"))
    ctx.axis1.set_ylabel(axes.get("y1").get("label"), color=axes.get("y1").get("color"))
    ctx.axis2.tick_params(axis='y', labelcolor=axes.get("y2").get("color"))
    ctx.axis2.set_ylabel(axes.get("y2").get("label"), color=axes.get("y2").get("color"))  # we already handled the x-label for y2 with axis1




def set_plot(ctx, data):
    """
    Updates the existing plot. 
    Detect whether checkboxes are checked, and display corresponding param curve accordingly.
    """
    try:
        visible_y1 = set()
        visible_y2 = set()
        for param_name, specs in ctx.config.get("params").items():
            if ctx.checkboxes_checked[param_name].get() == 1:
                ctx.curves[param_name].set_xdata(data.get("time"))
                ctx.curves[param_name].set_ydata(data.get(param_name))
                if specs.get("axis") == "y1":    
                    visible_y1.add(param_name)
                elif specs.get("axis") == "y2":    
                    visible_y2.add(param_name)

        # Get axis min/max values
        x_min, x_max = get_minmax(data.get("time"))
        y1_min, y1_max = get_ultimate_minmax(data, visible_y1)
        y2_min, y2_max = get_ultimate_minmax(data, visible_y2)

        # # Set axis ranges with some padding
        ctx.axis1.set_xlim([x_min, x_max*1.05])
        ctx.axis1.set_ylim([y1_min*0.95, y1_max*1.05])
        ctx.axis2.set_ylim([y2_min*0.95, y2_max*1.05]) # Second y-axis
        ctx.canvas.draw()
    except Exception as e:
        print("Exception in set_plot().", e)






def get_minmax(datalist):
    """
    None element throws an error, but np.nan does not.
    Exception thrown when np.nan is only element in the list. In this case, return 0,0.
    """
    return clean_axis_minmax(min(datalist)), clean_axis_minmax(max(datalist))



def get_ultimate_minmax(data, visible):
    # for all curves plotted on y-axis. Find the minimum of all minima, and maximum of all maxima.
    try:  
        y_min = clean_axis_minmax(min([min(val_list) for key,val_list in data.items() if key in visible]))
        y_max = clean_axis_minmax(max([max(val_list) for key,val_list in data.items() if key in visible])) 
    except:
        y_min, y_max = 0,0   
    return y_min, y_max



def clean_axis_minmax(val):
    """ Axis min/max cannot be None or np.NaN. Change these to 0. """ 
    return 0 if val is None or np.isnan(val) else val


def update_plot(ctx):
    ctx.axis1.cla()
    ctx.axis2.cla()
    start_plot(ctx, ctx.plotdata)   
    ctx.canvas.draw() #ctx.update()


# def resize_axes(ctx):
#     ctx.axis1.set_xlim([0,1])
#     ctx.axis1.set_ylim([0,1])
#     ctx.axis2.set_ylim([0,1])
