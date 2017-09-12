import numpy

gravity = 9.7915 # [m/s] at florianopolis

# pipe geometric charactics
pipe_length = 0.5 # [m]
pipe_external_diameter = 22.04E-3 # [m]
pipe_thickness = 0.9E-3 # [m]
pipe_inclination = 0 # rad
pipe_thermal_conduction = 237 # [W/(m*K]
kw = 237

# mesh geometric characteristics
mesh_wire_diameter = 28.06E-6 # [m]
mesh_opening_length = 102.09E-6 # [m]

# heat pipe construction characteristics
fluid = "Ethanol"
length_evaporator = 0.2 # [m]
length_adiabatic = 0.1 # [m]
length_condenser = 0.2 # [m]
number_of_mesh_layers = 5
crimp_factor = 1.0
minimal_operation_temperature = 40 + 273.15 # [K]
maximum_operation_temperature = 70 + 273.15 # [K]
temperature_operation = 40 + 273.15 # [K]
heat_transference = 80 # [W]

# Environment conditions
temperature_environment = 25 + 273.15 # [K]
pressure_environment = 101325 # [Pa]

# pipe geometric parameters calculations
mesh_number = 1 / (mesh_wire_diameter + mesh_opening_length)
epsilon = 1 - (crimp_factor * numpy.pi * mesh_number * mesh_wire_diameter / 4)
mesh_permeability = mesh_wire_diameter**2 * epsilon**3 / (122 * (1-epsilon)**2)
mesh_effective_capilar_radius = 1/(2*mesh_number)

pipe_external_radius = pipe_external_diameter/2
pipe_internal_diameter = pipe_external_diameter - 2*pipe_thickness
pipe_internal_radius = pipe_internal_diameter/2
pipe_effective_length = (length_condenser + length_evaporator)/2 + length_adiabatic

radius_steam = pipe_internal_radius - (crimp_factor * number_of_mesh_layers * mesh_wire_diameter)
diameter_steam = 2*radius_steam
area_solid = numpy.pi*(pipe_external_radius**2 - pipe_internal_radius**2)
area_liquid = numpy.pi * (pipe_internal_radius**2 - radius_steam**2)
area_steam = numpy.pi * radius_steam**2
perimeter_steam = 2 * numpy.pi * radius_steam
volume_liquid = area_liquid * pipe_length * epsilon
volume_steam = area_steam * pipe_length

area_evaporator = numpy.pi*pipe_external_diameter*length_evaporator
area_condenser = numpy.pi*pipe_external_diameter*length_condenser

# verifications
if pipe_length != (length_evaporator+length_adiabatic+length_condenser):
    raise ValueError("pipe length incompatible with evaporator+adiabatic+condenser lengths.")

if __name__ == "__main__":

    csvFile = open("calculated_geometric_parameters.csv","w")

    def summary():
        csvFile.write("{},{:g},{}\n".format("mesh_number", mesh_number, "m^(-1)"))
        csvFile.write("{},{:g},{}\n".format("epsilon", epsilon, "1"))
        csvFile.write("{},{:g},{}\n".format("mesh_permeability", mesh_permeability, "m^2"))
        csvFile.write("{},{:g},{}\n".format("mesh_effective_capilar_radius", mesh_effective_capilar_radius, "m"))
        csvFile.write("{},{:g},{}\n".format("pipe_internal_diameter", pipe_internal_diameter, "m"))
        csvFile.write("{},{:g},{}\n".format("pipe_internal_radius", pipe_internal_radius, "m"))
        csvFile.write("{},{:g},{}\n".format("pipe_effective_length", pipe_effective_length, "m"))
        csvFile.write("{},{:g},{}\n".format("radius_steam", radius_steam, "m"))
        csvFile.write("{},{:g},{}\n".format("diameter_steam", diameter_steam, "m"))
        csvFile.write("{},{:g},{}\n".format("area_liquid", area_liquid, "m^2"))
        csvFile.write("{},{:g},{}\n".format("area_steam", area_steam, "m^2"))
        csvFile.write("{},{:g},{}\n".format("perimeter_steam", perimeter_steam, "m"))
        csvFile.write("{},{:g},{}\n".format("volume_liquid", volume_liquid, "m^3"))
        csvFile.write("{},{:g},{}\n".format("volume_steam", volume_steam, "m^3"))
        csvFile.write("{},{:g},{}\n".format("area_evaporator", area_evaporator, "m^2"))
        csvFile.write("{},{:g},{}\n".format("area_evaporator", area_evaporator, "m^2"))

    summary()

    csvFile.close()
