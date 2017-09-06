import numpy
import matplotlib.pyplot as plt
from heat_pipe_data import *
from CoolProp.CoolProp import PropsSI

R = 8.3144621 # [J/(K mol)]
minimal_temperature = -20 + 273.15
maximum_temperature = 100 + 273.15
temperature = numpy.arange(minimal_temperature, maximum_temperature, 5)

max_capilar_heat = numpy.zeros(len(temperature))
for i in numpy.arange(len(temperature)):
    # maximum capilar pressure
    sigma = PropsSI("I", "T", temperature[i], "Q", 0, fluid)
    rho_liquid = PropsSI("D", "T", temperature[i], "Q", 0, fluid)
    radius_capilar = 1/(2*mesh_number)
    maximum_capilar_pressure = 2*sigma/radius_capilar

    # liquid friction factor
    viscosity_liquid = PropsSI("V", "T", temperature[i], "Q", 0, fluid)
    enthalpy_liquid = PropsSI("H", "T", temperature[i], "Q", 0, fluid)
    enthalpy_steam = PropsSI("H", "T", temperature[i], "Q", 1, fluid)
    enthalpy_evaporation = enthalpy_steam - enthalpy_liquid
    friction_factor_liquid = viscosity_liquid / (mesh_permeability * area_liquid * enthalpy_evaporation * rho_liquid)

    # steam friction factor
    correction_factor = 1
    fanning_laminar_friction = 16
    viscosity_steam = PropsSI("V", "T", temperature[i], "Q", 1, fluid)
    radius_hidraulic_steam = 2*radius_steam/2
    rho_steam = PropsSI("D", "T", temperature[i], "Q", 1, fluid)
    friction_factor_steam = correction_factor * fanning_laminar_friction * viscosity_steam / (2 * radius_hidraulic_steam * area_steam * rho_steam * enthalpy_evaporation)

    max_capilar_heat[i] = (maximum_capilar_pressure - rho_liquid * gravity * pipe_length * numpy.sin(pipe_inclination)) / (friction_factor_liquid - friction_factor_steam)
    #q_capf(i)=((pc_max(i)-(rho_l(i)*g*l*sind(psi)))/(f_l(i)+f_v(i)));%/(1000);%Q_capilar livro de Faghri, pag 227

# sonic limit
max_sonic_heat = numpy.zeros(len(temperature))
for i in numpy.arange(len(temperature)):
    rho_steam = PropsSI("D", "T", temperature[i], "Q", 1, fluid)
    enthalpy_liquid = PropsSI("H", "T", temperature[i], "Q", 0, fluid)
    enthalpy_steam = PropsSI("H", "T", temperature[i], "Q", 1, fluid)
    enthalpy_evaporation = enthalpy_steam - enthalpy_liquid
    specific_heat_pressure = PropsSI("C", "T", temperature[i], "Q", 1, fluid)
    specific_heat_volume = PropsSI("O", "T", temperature[i], "Q", 1, fluid)
    gamma_steam = specific_heat_pressure / specific_heat_volume
    molar_mass = PropsSI(fluid, "molemass")
    R_steam = R / molar_mass

    max_sonic_heat[i] = area_steam * rho_steam * enthalpy_evaporation * ( (gamma_steam * R_steam * temperature[i])/(2*gamma_steam+2) )**0.5
    #q_s(i)=((a_v*rho_v(i)*hlv(i))*(((gamma*rv*T_t(i))/(2*(gamma+1)))^(0.5)));%/(1000);%%temperatura es en K

# Boiling limit
max_boiling_heat = numpy.zeros(len(temperature))
for i in numpy.arange(len(temperature)):
    conductivity_liquid = PropsSI("L", "T", temperature[i], "Q", 0, fluid)
    conductivity_steam = PropsSI("L", "T", temperature[i], "Q", 1, fluid)
    kl = conductivity_liquid
    kw = 237
    conductivity_effective = kl * ((kl+kw)-(1-epsilon)*(kl-kw)) / ( (kl+kw)+(1-epsilon)*(kl-kw) )
    sigma = PropsSI("I", "T", temperature[i], "Q", 0, fluid)
    nucleation_critical_radius = 2.54E-7 # 2.54E-7 < nucleation_critical_radius < 2.54E-5 [m]
    radius_capilar = 1/(2*mesh_number)
    pressure_capilar = 2*sigma/radius_capilar

    enthalpy_liquid = PropsSI("H", "T", temperature[i], "Q", 0, fluid)
    enthalpy_steam = PropsSI("H", "T", temperature[i], "Q", 1, fluid)
    enthalpy_evaporation = enthalpy_steam - enthalpy_liquid
    rho_steam = PropsSI("D", "T", temperature[i], "Q", 1, fluid)

    max_boiling_heat[i] = 2 * numpy.pi * length_evaporator * conductivity_effective * temperature[i] * (2*sigma/nucleation_critical_radius - pressure_capilar) / (enthalpy_evaporation * rho_steam * numpy.log(pipe_internal_radius/radius_steam))
    # q_e(i)=(((2*pi*le*keff(i)*T_t(i))/(hlv(i)*rho_v(i)*(log((0.5*d_int)/r_v))))*(((2*ts(i))/rn)-pc_max(i)));

# Drag limit
max_drag_heat = numpy.zeros(len(temperature))
for i in numpy.arange(len(temperature)):
    enthalpy_liquid = PropsSI("H", "T", temperature[i], "Q", 0, fluid)
    enthalpy_steam = PropsSI("H", "T", temperature[i], "Q", 1, fluid)
    enthalpy_evaporation = enthalpy_steam - enthalpy_liquid
    sigma = PropsSI("I", "T", temperature[i], "Q", 0, fluid)
    rho_steam = PropsSI("D", "T", temperature[i], "Q", 1, fluid)
    radius_hidraulic = 1/(2*mesh_number) - mesh_wire_diameter/2

    max_drag_heat[i] = area_steam * enthalpy_evaporation * (sigma*rho_steam/(2*radius_hidraulic))**(1/2)
    # q_em(i)=((a_v*hlv(i))*(((ts(i)*rho_v(i))/(2*r_h_w))^(0.5)));

# Viscous limit
max_viscous_heat = numpy.zeros(len(temperature))
for i in numpy.arange(len(temperature)):
    enthalpy_liquid = PropsSI("H", "T", temperature[i], "Q", 0, fluid)
    enthalpy_steam = PropsSI("H", "T", temperature[i], "Q", 1, fluid)
    enthalpy_evaporation = enthalpy_steam - enthalpy_liquid
    rho_steam = PropsSI("D", "T", temperature[i], "Q", 1, fluid)
    pressure_steam = PropsSI("P", "T", temperature[i], "Q", 1, fluid)
    viscosity_steam = PropsSI("V", "T", temperature[i], "Q", 1, fluid)

    max_viscous_heat[i] = area_steam * (2*radius_steam)**2 * enthalpy_evaporation * rho_steam * pressure_steam / (64*viscosity_steam*pipe_effective_length)
    # q_v(i)=a_v*((((((2*r_v)^2)*hlv(i)*rho_v(i)*p0(i))/(64*nu_v(i)*lef))));

# plot
fig = plt.figure(1)
ax = fig.add_subplot(1,1,1)
temperature = temperature - 273.15
ax.semilogy(temperature,max_capilar_heat,'-kx')
ax.semilogy(temperature,max_sonic_heat,'-k*')
ax.semilogy(temperature,max_boiling_heat,'-ks')
ax.semilogy(temperature,max_drag_heat,'-ko')
ax.semilogy(temperature,max_viscous_heat,'-k^')
ax.grid(True)
ax.set_xlabel('Temperatura [C]')
ax.set_ylabel('Q [W]')
ax.legend(["Capilar", "Sonico","Ebulicao","Arrasto","Viscoso"])

plt.show()
