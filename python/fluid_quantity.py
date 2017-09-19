from CoolProp.CoolProp import PropsSI
from heat_pipe_data import *

# fluid quantity calculation
rho_liquid = PropsSI('D', 'T', temperature_operation, 'Q', 0, fluid)
rho_steam = PropsSI('D', 'T', temperature_operation, 'Q', 1, fluid)
mass_liquid = rho_liquid * volume_liquid
mass_steam = rho_steam * volume_steam
mass_total = mass_liquid + mass_steam

rho_environment = PropsSI('D', 'T', temperature_environment, 'P', pressure_environment, fluid)
volume_environment = mass_total / rho_environment
volume_environment_in_ml = volume_environment * 1E+6

def print_fluid_quantity(message, quantity_in_ml):
    print("{:45} = {:4.3g} [ml]".format(message, quantity_in_ml))

print_fluid_quantity("epsilon",epsilon)
print_fluid_quantity("area_liquid * pipe_length", 1E+6*(area_liquid*pipe_length))
print("\n")

print_fluid_quantity("volume ocupado pelo liquido", 1E+6*volume_liquid)
print_fluid_quantity("volume ocupado pelo vapor", 1E+6*volume_steam)
print("\n")

print("Proposta do Nelson:")
print_fluid_quantity("Volume necessario no meio poroso:", 1E+6*volume_liquid)
print_fluid_quantity("110% do volume necessario no meio poroso:", 1E+6*1.1*volume_liquid)
print("\n")

print("Nossa proposta:")
print_fluid_quantity("Volume necessario", volume_environment_in_ml)
print_fluid_quantity("110% do Volume necessario", 1.1*volume_environment_in_ml)
