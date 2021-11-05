from tkinter import *
import numpy as np
import chart 



LABEL_RELX = 0.73


def build_buttons(ctx):
    reset_button = Button(ctx, text="Reset", command=ctx.reset)
    reset_button.place(relx=0.96, rely=0.1, anchor=E, width=85)

    save_button = Button(ctx, text="Save", command=ctx.save)
    save_button.place(relx=0.96, rely=0.2, anchor=E, width=85)

    saveas_button = Button(ctx, text="Save As...", command=ctx.saveas)
    saveas_button.place(relx=0.96, rely=0.3, anchor=E, width=85)

    exit_button = Button(ctx, text="Exit", command=ctx.exit)
    exit_button.place(relx=0.96, rely=0.85, anchor=E, width=85)




def build_output_labels(ctx):
    ctx.label_time = create_output_label(ctx, "Time (s)", relx=LABEL_RELX, name_y=0.05, output_y=0.1)  
    ctx.labels = {
        "p1": create_output_label(ctx, "Pressure (psig)", relx=LABEL_RELX, name_y=0.2, output_y=0.25),
        "t1": create_output_label(ctx, "Temperature 1 (\u00B0C)", relx=LABEL_RELX, name_y=0.35, output_y=0.4),
        "t2": create_output_label(ctx, "Temperature 2 (\u00B0C)", relx=LABEL_RELX, name_y=0.5, output_y=0.55),
        "t3": create_output_label(ctx, "Temperature 3 (\u00B0C)", relx=LABEL_RELX, name_y=0.65, output_y=0.7),
        "t4": create_output_label(ctx, "Temperature 4 (\u00B0C)", relx=LABEL_RELX, name_y=0.8, output_y=0.85)
    }



def create_output_label(ctx, name, relx, name_y, output_y):
    ctx.title = Label(ctx, text=name)
    ctx.title.place(relx=relx, rely=name_y, anchor=E)
    ctx.label = Label(ctx, text="", anchor='e')
    ctx.label.config(font=("calibre", 18), fg="#fff", background="#000")
    ctx.label.place(relx=relx, rely=output_y, anchor=E, width=100)
    return ctx.label



def output_reading(label, reading):
    # Output reading to a label
    if np.isnan(reading):
        label.config(text="-")
    else:
        label.config(text=reading)




def build_checkboxes(ctx):
    CHECK_RELX = LABEL_RELX - 0.10
    # Create checkboxes here.
    ctx.checkboxes= {
        "p1": None,
        "t1": None,
        "t2": None,
        "t3": None,
        "t4": None,
        }
    # Checkbox variables, controller needs access 
    ctx.checkboxes_checked = {
        "p1": IntVar(),
        "t1": IntVar(),
        "t2": IntVar(),
        "t3": IntVar(),
        "t4": IntVar(),
        }
    create_checkbox(ctx, name="p1", relx=CHECK_RELX, rely=0.25, bgcolor=ctx.legend.get("p1"))
    create_checkbox(ctx, name="t1", relx=CHECK_RELX, rely=0.4, bgcolor=ctx.legend.get("t1"))
    create_checkbox(ctx, name="t2", relx=CHECK_RELX, rely=0.55, bgcolor=ctx.legend.get("t2"))
    create_checkbox(ctx, name="t3", relx=CHECK_RELX, rely=0.7, bgcolor=ctx.legend.get("t3"))
    create_checkbox(ctx, name="t4", relx=CHECK_RELX, rely=0.85, bgcolor=ctx.legend.get("t4"))



def create_checkbox(ctx, name, relx, rely, bgcolor):
    ctx.checkboxes[name] = Checkbutton(ctx, command=lambda cb_num=name: check_status(ctx, cb_num, bgcolor), variable=ctx.checkboxes_checked[name])
    ctx.checkboxes[name]['background'] = bgcolor
    ctx.checkboxes[name].config()
    ctx.checkboxes[name].select()
    ctx.checkboxes[name].place(relx=relx, rely=rely, anchor=E) 


def check_status(ctx, cb_num, bgcolor):
    """ Check the status of the checkbox: 1 or 0 """
    if ctx.checkboxes_checked[cb_num].get() == 1:
        ctx.checkboxes[cb_num]['background'] = bgcolor #ctx.legend.get(ctx.params.get(cb_num))
    else:
        ctx.checkboxes[cb_num]['background'] = "#e9e9e9" # grey
    chart.update_plot(ctx)



def build_message(ctx):
    """ For error messaging, etc. """
    ctx.message = Label(ctx, text="")
    ctx.message.place(relx=0.96, rely=0.4, anchor=E)
   
    # Create function for displaying messages
    def show_message(message):
        ctx.message.config(text=message)
        ctx.message_timer = 10
    ctx.show_message = show_message 