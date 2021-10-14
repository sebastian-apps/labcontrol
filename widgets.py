from tkinter import *
import numpy as np
import chart 



LABEL_RELX = 0.73


def build_buttons(self):
    reset_button = Button(self, text="Reset", command=self.reset)
    reset_button.place(relx=0.96, rely=0.1, anchor=E, width=85)

    save_button = Button(self, text="Save", command=self.save)
    save_button.place(relx=0.96, rely=0.2, anchor=E, width=85)

    saveas_button = Button(self, text="Save As...", command=self.saveas)
    saveas_button.place(relx=0.96, rely=0.3, anchor=E, width=85)

    exit_button = Button(self, text="Exit", command=self.exit)
    exit_button.place(relx=0.96, rely=0.85, anchor=E, width=85)




def build_output_labels(self):
    self.label_time = create_output_label(self, "Time (s)", relx=LABEL_RELX, name_y=0.05, output_y=0.1)  
    self.labels = {
        "p1": create_output_label(self, "Pressure (psig)", relx=LABEL_RELX, name_y=0.2, output_y=0.25),
        "t1": create_output_label(self, "Temperature 1 (\u00B0C)", relx=LABEL_RELX, name_y=0.35, output_y=0.4),
        "t2": create_output_label(self, "Temperature 2 (\u00B0C)", relx=LABEL_RELX, name_y=0.5, output_y=0.55),
        "t3": create_output_label(self, "Temperature 3 (\u00B0C)", relx=LABEL_RELX, name_y=0.65, output_y=0.7),
        "t4": create_output_label(self, "Temperature 4 (\u00B0C)", relx=LABEL_RELX, name_y=0.8, output_y=0.85)
    }



def create_output_label(self, name, relx, name_y, output_y):
    self.title = Label(self, text=name)
    self.title.place(relx=relx, rely=name_y, anchor=E)
    self.label = Label(self, text="", anchor='e')
    self.label.config(font=("calibre", 18), fg="#fff", background="#000")
    self.label.place(relx=relx, rely=output_y, anchor=E, width=100)
    return self.label



def output_reading(label, reading):
    # Output reading to a label
    if np.isnan(reading):
        label.config(text="-")
    else:
        label.config(text=reading)




def build_checkboxes(self):
    CHECK_RELX = LABEL_RELX - 0.10
    # Checkbox variables, controller needs access 
    self.checkboxes_checked = [IntVar() for _ in range(self.params_num)]
    # Create checkboxes here.
    self.checkboxes = [i for i in range(self.params_num)]
    create_checkbox(self, num=0, relx=CHECK_RELX, rely=0.25, bgcolor=self.legend.get("p1"))
    create_checkbox(self, num=1, relx=CHECK_RELX, rely=0.4, bgcolor=self.legend.get("t1"))
    create_checkbox(self, num=2, relx=CHECK_RELX, rely=0.55, bgcolor=self.legend.get("t2"))
    create_checkbox(self, num=3, relx=CHECK_RELX, rely=0.7, bgcolor=self.legend.get("t3"))
    create_checkbox(self, num=4, relx=CHECK_RELX, rely=0.85, bgcolor=self.legend.get("t4"))



def create_checkbox(self, num, relx, rely, bgcolor):
    self.checkboxes[num] = Checkbutton(self, command=lambda cb_num=num: check_status(self, cb_num, bgcolor), variable=self.checkboxes_checked[num])
    self.checkboxes[num]['background'] = bgcolor
    self.checkboxes[num].config()
    self.checkboxes[num].select()
    self.checkboxes[num].place(relx=relx, rely=rely, anchor=E) 


def check_status(self, cb_num, bgcolor):
    """ Check the status of the checkbox: 1 or 0 """
    if self.checkboxes_checked[cb_num].get() == 1:
        self.checkboxes[cb_num]['background'] = bgcolor #self.legend.get(self.params.get(cb_num))
    else:
        self.checkboxes[cb_num]['background'] = "#e9e9e9" # grey
    chart.update_plot(self)



def build_message(self):
    """ For error messaging, etc. """
    self.message = Label(self, text="")
    self.message.place(relx=0.96, rely=0.4, anchor=E)
   
    # Create function for displaying messages
    def show_message(message):
        self.message.config(text=message)
        self.message_timer = 10
    self.show_message = show_message 