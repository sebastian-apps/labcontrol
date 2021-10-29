import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
import numpy as np


def setup(ctx):
    """ Set up matplotlib plotting canvas and layout. """
    ctx.curves = [i for i in range(ctx.params_num)]
    ctx.f = Figure(figsize=(6,5), dpi=100)
    ctx.axis1 = ctx.f.add_subplot(111)
    ctx.axis2 = ctx.axis1.twinx()  # create a second y-axis
    # ctx.axis1.set_xlim([0, 200]);
    # ctx.axis1.set_ylim([0, 200]);
    ax_plot(ctx, ctx.plotdata)
    ctx.canvas = FigureCanvasTkAgg(ctx.f, ctx)
    ctx.canvas.get_tk_widget().pack(anchor='w', fill=BOTH, expand=YES)
    ctx.canvas.get_tk_widget().place(x=5, y=25)
    ctx.canvas._tkcanvas.pack(anchor='w', fill=BOTH, expand=YES)
    ctx.canvas._tkcanvas.place(x=5, y=25)
    ctx.f.tight_layout() # otherwise the right y-label is slightly clipped




def ax_plot(ctx, data):
    """ 
    Plot the axes and values. This method is called when first creating the plot.
    For plot updates, call set_plot(...)
    Detect whether checkboxes are checked, and display corresponding output curve accordingly.
    """
    # PRIMARY Y-AXIS
    for i in range(ctx.params_num):
        param_name = ctx.params.get(i)
        if i != 0: # Exclude because i=0 is plotted on the secondary y-axis
            if ctx.checkboxes_checked[i].get() == 1:
                ctx.curves[i], = ctx.axis1.plot(
                                                data.get("time"), 
                                                data.get(param_name), 
                                                color=ctx.legend.get(param_name), 
                                                linewidth=1, 
                                                alpha=0.7)
    ctx.axis1.set_xlabel('Time (s)')
    ctx.axis1.set_ylabel('Temperature (\u00B0C)')

    # SECONDARY Y-AXIS
    if ctx.checkboxes_checked[0].get() == 1:
        ctx.curves[0], = ctx.axis2.plot(
                                        data.get("time"),
                                        data.get("p1"), 
                                        color=ctx.legend.get("p1"), 
                                        linewidth=1, 
                                        alpha=0.7)
    ctx.axis2.tick_params(axis='y', labelcolor='b')
    ctx.axis2.set_ylabel('Pressure (psig)', color='b')  # we already handled the x-label with ax1




def set_plot(ctx, data):
    """
    Updates the existing plot. 
    Detect whether checkboxes are checked, and display corresponding param curve accordingly.
    """
    try:
        visible = set()
        for i in range(ctx.params_num):
            if i != 0: # Exclude because i=0 is plotted on the second y-axis
                param_name = ctx.params.get(i)
                if ctx.checkboxes_checked[i].get() == 1:
                    ctx.curves[i].set_xdata(data.get("time"))
                    ctx.curves[i].set_ydata(data.get(param_name))
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
        if ctx.checkboxes_checked[0].get() == 1:
            ctx.curves[0].set_xdata(data.get("time"))
            ctx.curves[0].set_ydata(data.get("p1"))

        # # Set axis ranges with some padding
        ctx.axis1.set_xlim([x_min, x_max*1.05])
        ctx.axis1.set_ylim([y_min*0.95, y_max*1.05])
        ctx.axis2.set_ylim([y2_min*0.95, y2_max*1.05]) # Second y-axis
        ctx.canvas.draw()
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


def update_plot(ctx):
    ctx.axis1.cla()
    ctx.axis2.cla()
    ax_plot(ctx, ctx.plotdata)   
    ctx.canvas.draw() #ctx.update()


# def resize_axes(ctx):
#     ctx.axis1.set_xlim([0,1])
#     ctx.axis1.set_ylim([0,1])
#     ctx.axis2.set_ylim([0,1])
