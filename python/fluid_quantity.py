from CoolProp.CoolProp import PropsSI
import numpy

# evaporator_length = 0.2
# adiabatic_length = 0.1
# condenser_length = 0.2

# User data
fluid = "Ethanol"
temperature_operation = 50 + 273.15 # [K]
pipe_external_diameter = 22.04E-3 # [m]
pipe_thickness = 0.9E-3 # [m]
pipe_length = 0.5 # [m]
wire_diameter = 28.06E-6 # [m]
opening_length = 102.09E-6 # [m]
number_of_mesh_turns = 5.0
crimp_factor = 1.05

# pipe geometric parameters calculations
mesh_number = 1 / (wire_diameter + opening_length)
epsilon = 1 - (crimp_factor * numpy.pi * mesh_number * wire_diameter / 4)

internal_radius = pipe_external_diameter / 2 - pipe_thickness
radius_till_mesh = internal_radius - (crimp_factor * number_of_mesh_turns * wire_diameter)

area_liquid = numpy.pi * (internal_radius**2 - radius_till_mesh**2)
area_steam = numpy.pi * radius_till_mesh**2

volume_liquid = area_liquid * pipe_length * epsilon
volume_steam = area_steam * pipe_length

# fluid quantity calculation
rho_liquid = PropsSI('D', 'T', temperature_operation, 'Q', 0, fluid)
rho_steam = PropsSI('D', 'T', temperature_operation, 'Q', 1, fluid)
mass_liquid = rho_liquid * volume_liquid
mass_steam = rho_steam * volume_steam
mass_total = mass_liquid + mass_steam

temperature_environment = 25 + 273.15 # [K]
pressure_environment = 101325 # [Pa]
rho_environment = PropsSI('D', 'T', temperature_environment, 'P', pressure_environment, fluid)
volume_environment = mass_total / rho_environment
volume_environment_in_ml = volume_environment * 1E+6

print("{} = {} [m3] = {} [ml]".format("Volume necessario", volume_environment, volume_environment_in_ml))
print("{} = {} [m3] = {} [ml]".format("110 % do Volume necessario", 1.1*volume_environment, 1.1*volume_environment_in_ml))
print("{} {} {}".format("Volume necessario usando o volume do meio poroso:", 1E+6*volume_liquid, "[ml]"))
print("{} {} {}".format("Volume necessario usando 110%% do volume do meio poroso:", 1E+6*1.1*volume_liquid, "[ml]"))
