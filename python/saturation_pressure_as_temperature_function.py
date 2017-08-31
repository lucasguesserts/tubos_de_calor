from CoolProp.CoolProp import *
from numpy import *
import matplotlib.pyplot as plt

# User settings
temperature = arange(10,101,10)
fluid = "Water"

def saturationPressure( temperature, fluid ):
    n_temp = len(temperature)
    pressure = zeros(n_temp)
    for i in range(n_temp):
        kelvin_temperature = temperature[i] + 273.15
        pressure[i] = PropsSI('P','T',kelvin_temperature,'Q',1,fluid)
    return pressure

def plotSaturationPressure( temperature, fluid, fig_number ):
    fig = plt.figure(fig_number)
    pressure = saturationPressure(temperature, fluid)
    ax = fig.add_subplot(111)
    ax.plot(temperature, pressure)
    title = fluid + " saturation pressure"
    ax.set_title(title)
    ax.set_ylabel("Pressure [Pa]")
    ax.set_xlabel("Temperature [C]")
    ax.set_yscale("log")
    ax.grid(True, which="both")
    filename = fluid + "_log.png"
    fig.savefig(filename)

# plot
ax_number = 1
plotSaturationPressure( temperature, fluid, ax_number )
plt.show()
