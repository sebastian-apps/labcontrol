# LabControl

LabControl is software designed to monitor and control your process equipment in a laboratory or plant. 
Consolidate all your sensor and controller output data and plot the data real-time for monitoring processes. 
Temperature, pressure, mass, voltage, and any other reading from your process equipment can be integrated into LabControl.
Data can also be exported for future analysis.

The software is currently set up to read from a pressure transducer and four thermocouples.
However, the software can be easily modified to suit your needs. 

Tkinter is used for the Python GUI. Plotting is performed using matplotlib. 
The serial and minimalmodbus packages are used for communicating with sensors and controllers.

Future versions will include options to write setpoint values to the controller.
<br />

## Set up and Run

Clone the repository.

```
git clone https://github.com/sebastian-apps/labcontrol.git
```

Create the virtual environment.

```
cd labcontrol
python -m venv labcontrol_env
```

Activate the virtual environment for OSX.

```
source labcontrol_env/bin/activate
```

Activate the virtual environment for Windows.

```
labcontrol_env\Scripts\activate
```

Install dependencies. 

```
pip install -r requirements.txt
```

Run LabControl.

```
python labcontrol.py
```

