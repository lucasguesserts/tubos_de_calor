from heat_pipe_data import *
from CoolProp.CoolProp import PropsSI

# A precise model is needed for
# external evaporator resistance;
# It will depend on our system,
# how it is build.
R_ext_e = 0

# A precise model is needed for
# external condenser resistance;
# It will depend on our system,
# how it is build.
R_ext_c = 0

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

    csvFile = open("thermal_resistances.csv","w")

    def summary():
        thermal_resistance_unit = "K/W"
        csvFile.write("{},{:g},{}\n".format("Rpe", Rpe, thermal_resistance_unit))
        csvFile.write("{},{:g},{}\n".format("Rpc", Rpc, thermal_resistance_unit))
        csvFile.write("{},{:g},{}\n".format("Rwe", Rwe, thermal_resistance_unit))
        csvFile.write("{},{:g},{}\n".format("Rwc", Rwc, thermal_resistance_unit))
        csvFile.write("{},{:g},{}\n".format("Rie", Rie, thermal_resistance_unit))
        csvFile.write("{},{:g},{}\n".format("Ric", Ric, thermal_resistance_unit))
        csvFile.write("{},{:g},{}\n".format("Rva", Rva, thermal_resistance_unit))
        csvFile.write("{},{:g},{}\n".format("Rpa", Rpa, thermal_resistance_unit))
        csvFile.write("{},{:g},{}\n".format("Rwa", Rwa, thermal_resistance_unit))
        csvFile.write("{},{:g},{}\n".format("Rwa", Rwa, thermal_resistance_unit))
        csvFile.write("{},{:g},{}\n".format("Rp", Rp, thermal_resistance_unit))
        csvFile.write("{},{:g},{}\n".format("Rw", Rw, thermal_resistance_unit))
        csvFile.write("{},{:g},{}\n".format("Rv", Rv, thermal_resistance_unit))
        csvFile.write("{},{:g},{}\n".format("Rt", Rt, thermal_resistance_unit))
        csvFile.write("{},{:g},{}\n".format("R_ext_e", R_ext_e, thermal_resistance_unit))
        csvFile.write("{},{:g},{}\n".format("R_ext_c", R_ext_c, thermal_resistance_unit))

    summary()

    csvFile.close()
