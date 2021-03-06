from heat_pipe_data import *
from CoolProp.CoolProp import PropsSI

# A precise model is needed for
# external evaporator resistance;
# It will depend on our system,
# how it is build.
R_ext_e = 0

# condenser resistance
def correlation_C(Re_D):
    if  0.4 <= Re_D < 4.0:
        return 0.989
    elif 4.0 <= Re_D < 40:
        return 0.911
    elif 40 <= Re_D < 4000:
        return 0.683
    elif 4000 <= Re_D < 40000:
        return 0.193
    elif 40000 <= Re_D < 400000:
        return 0.027
    else:
        raise ValueError("invalid Re_D value inserted in function \'C\'")

def correlation_m(Re_D):
    if  0.4 <= Re_D < 4.0:
        return 0.330
    elif 4.0 <= Re_D < 40:
        return 0.385
    elif 40 <= Re_D < 4000:
        return 0.466
    elif 4000 <= Re_D < 40000:
        return 0.618
    elif 40000 <= Re_D < 400000:
        return 0.805
    else:
        raise ValueError("invalid Re_D value inserted in function \'m\'")

def h(V, D, temperature):
    fluid = "Air"
    pressure = 101325
    k = PropsSI("L", "T", temperature, "P", pressure, fluid)
    cp = PropsSI("C", "T", temperature, "P", pressure, fluid)
    rho = PropsSI("D", "T", temperature, "P", pressure, fluid)
    mu = PropsSI("V", "T", temperature, "P", pressure, fluid)

    Re_D = rho * V * D / mu
    Pr = cp * mu / k
    C = correlation_C(Re_D)
    m = correlation_m(Re_D)

    Nu = C * Re_D**m * Pr**(1/3)
    h = Nu * k / D
    return h

fluid_velocity = 7.0
condenser_area = numpy.pi * pipe_external_diameter**2 / 4
environment_temperature = 25 + 273.15
film_temperature = (environment_temperature + temperature_operation) / 2
h_condenser = h(fluid_velocity, pipe_external_diameter, film_temperature)
R_ext_c = 1 / (h_condenser * condenser_area)

# Needed properties
R = 8.3144621 # [J/(K mol)]
molar_mass = PropsSI(fluid, "molemass")
R_fluid = R / molar_mass
enthalpy_liquid = PropsSI("H", "T", temperature_operation, "Q", 0, fluid)
enthalpy_steam = PropsSI("H", "T", temperature_operation, "Q", 1, fluid)
enthalpy_evaporation = enthalpy_steam - enthalpy_liquid
pressure_saturation = PropsSI("P", "T", temperature_operation, "Q", 1, fluid)
pressure_difference_between_evaporator_and_condenser = 1E-6
conductivity_liquid = PropsSI("L", "T", temperature_operation, "Q", 0, fluid)
conductivity_steam = PropsSI("L", "T", temperature_operation, "Q", 1, fluid)
kl = conductivity_liquid
kw = pipe_thermal_conduction
conductivity_effective = kl * ((kl+kw)-(1-epsilon)*(kl-kw)) / ( (kl+kw)+(1-epsilon)*(kl-kw) )

# Atomic thermal resistances
Rpe = numpy.log(pipe_external_diameter/pipe_internal_diameter) / (2*numpy.pi*length_evaporator*pipe_thermal_conduction)
Rpc = numpy.log(pipe_external_diameter/pipe_internal_diameter) / (2*numpy.pi*length_condenser*pipe_thermal_conduction)
Rwe = numpy.log(pipe_internal_diameter/diameter_steam) / (2*numpy.pi*length_evaporator*conductivity_effective)
Rwc = numpy.log(pipe_external_diameter/pipe_internal_diameter) / (2*numpy.pi*length_condenser*conductivity_effective)
Rie = (R_fluid * temperature_operation**2) * (2*numpy.pi*R_fluid*temperature_operation)**(1/2) / (enthalpy_evaporation**2 * pressure_saturation * area_evaporator)
Ric = (R_fluid * temperature_operation**2) * (2*numpy.pi*R_fluid*temperature_operation)**(1/2) / (enthalpy_evaporation**2 * pressure_saturation * area_condenser)
Rva = R_fluid * temperature_operation**2 * pressure_difference_between_evaporator_and_condenser / (enthalpy_evaporation * pressure_saturation * heat_transference)
Rpa = pipe_effective_length / (pipe_thermal_conduction * area_solid)
Rwa = pipe_effective_length / (conductivity_effective * area_liquid)

Rp = Rpe/2 + Rpa + Rpc/2
Rw = Rpe + Rwe/2 + Rwa + Rwc/2 + Rpc
Rv = Rpe + Rwe + Rie + Rva + Ric + Rwc + Rpc
Rt = R_ext_e + (1/Rp + 1/Rw + 1/Rv)**(-1) + R_ext_c


if __name__ == "__main__":

    thermal_resistance_unit = "K/W"
    csvFile = open("thermal_resistances.csv","w")
    dataMatrix = [
        ["Rpe", Rpe, thermal_resistance_unit],
        ["Rpc", Rpc, thermal_resistance_unit],
        ["Rwe", Rwe, thermal_resistance_unit],
        ["Rwc", Rwc, thermal_resistance_unit],
        ["Rie", Rie, thermal_resistance_unit],
        ["Ric", Ric, thermal_resistance_unit],
        ["Rva", Rva, thermal_resistance_unit],
        ["Rpa", Rpa, thermal_resistance_unit],
        ["Rwa", Rwa, thermal_resistance_unit],
        ["Rwa", Rwa, thermal_resistance_unit],
        ["Rp", Rp, thermal_resistance_unit],
        ["Rw", Rw, thermal_resistance_unit],
        ["Rv", Rv, thermal_resistance_unit],
        ["Rt", Rt, thermal_resistance_unit],
        ["R_ext_e", R_ext_e, thermal_resistance_unit],
        ["R_ext_c", R_ext_c, thermal_resistance_unit]
    ]

    summary(csvFile, dataMatrix)

    csvFile.close()
