import numpy

fluid = "Ethanol"
temperature_operation = 50 + 273.15 # [K]

length_evaporator = 0.2
length_adiabatic = 0.1
length_condenser = 0.2

# User data
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
