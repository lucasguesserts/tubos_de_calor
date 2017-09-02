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

print("{} = {} [m3] = {} [ml]".format("Volume necessario", volume_environment, volume_environment_in_ml))
print("{} = {} [m3] = {} [ml]".format("110 % do Volume necessario", 1.1*volume_environment, 1.1*volume_environment_in_ml))
print("{} {} {}".format("Volume necessario usando o volume do meio poroso:", 1E+6*volume_liquid, "[ml]"))
print("{} {} {}".format("Volume necessario usando 110%% do volume do meio poroso:", 1E+6*1.1*volume_liquid, "[ml]"))
