import numpy
import matplotlib.pyplot as plt

%% Informa��o conhecida
le=0.3; %Comprimento do evaporador [m]
lad=0.1; %Comprimento da secao adibatica [m]
lc=0.5; %Comprimento do condensador [m]
l=le+lad+lc; %Comprimento total [m]
q=30; %Calor dissipado [W]
psi=-90;
xe=0:0.01:le; %Dominio do evaporador
xa=le:0.01:le+lad; %Dominio da se��o adibatica
xc=le+lad:0.01:l; %Dominio do condensador
lef=(lc+le)/2+lad; %Comprimento efetivo [m]

%% Carateristicas do tubo de calor
d_f=1.143e-4; % Diametro do fio da tela [m]
d_ext=31.75e-3; %Diametro exterior do tubo [m]
t=3.17e-3; %Espessura do tubo [m]
c=10; %# de camadas
b=1; % Fator do core��o do momento
cf=1; %C fator de corecao  
f_re=16; % Fator de atrito de Faning laminar
S=1.05; %Fator de crimpagem (Chi,1975)
N=100/0.0254; %N�mero de mesh
% r_v=(d_ext-2*t-(2*(c*d_f)))/2; %Raio do vapor [m]
esp=1;
r_v=(d_ext-2*t-(esp*2*(c*d_f)))/2; %Raio do vapor [m]
a_v=pi*(r_v)^2; %Area do vapor  [m^2]
d_int=d_ext-2*t;
g=9.81; %Gravedad
kw=237;
rn=2.54e-7; %Pressao capilar da estrutura
T_ope=40;%Temperatura de opera��o [C]
t_min=-20;
t_max=100;
n=25;
tm=linspace(t_min,t_max,n);% Con n=23, espacamento=5 C na temperatura
fluid="Acetone";

%% Propiedades do fluido (Coolprop)
%Acetona
for i=1:n %Temparetura de trabalho [K]
 T_t(i)=tm(i)+273.15;   
 p0(i)=Props('P','T',T_t(i),'Q',1,fluid)*1000;  
 rho_v(i)=Props('D','T',T_t(i),'Q',1,fluid);
 rho_l(i)=Props('D','T',T_t(i),'Q',0,fluid);
 nu_v(i)=Props('V','T',T_t(i),'Q',1,fluid);
 nu_l(i)=Props('V','T',T_t(i),'Q',0,fluid);
 h_v(i)=Props('H','T',T_t(i),'Q',1,fluid);
 h_l(i)=Props('H','T',T_t(i),'Q',0,fluid);
 ts(i)=Props('I','T',T_t(i),'Q',1,fluid);
 c_p(i)=Props('C','T',T_t(i),'P',p0,fluid);
 hlv(i)=(h_v(i)-h_l(i))*10^3;
 c_v(i)=Props('O','T',T_t(i),'P',p0,fluid);
 kl(i)=Props('L','T',T_t(i),'Q',0,fluid)*1000;
 kv(i)=Props('L','T',T_t(i),'Q',1,fluid)*1000;
end
% T_t=T_ope+273.15;%Temparetura de trabalho [K]

gamma=1.33; % Vapor poliatomico
r=8.314e3; %Constante universal dos gases
mm=Props(fluid,'molemass'); % Massa molar
rv=r/mm; %Constante do vapor

epsilon=1-((S*pi*N*d_f)/(4));
k=(((d_f)^2)*(epsilon^3))/(122*((1-epsilon)^2)); %Permeabilidade
a_w=(pi/4)*((d_ext-2*t)^2-(2*r_v)^2); %Area do liquido

temperature = numpy.arange(minimal_operation_temperature, maximal_operation_temperature, 5)
 
# Operations limits


# capilar limit
radius_capilar = 1/(2*mesh_number)

r_c=1/(2*N);% Raio capilar
delta_p_f=0; %Queda de pressao relativa a mudanca de fase
r_h_v=(r_v*2)/(2); %Raio hidraulico do escoamento do vapor
for i=1:n 
pc_max(i)=(2*ts(i))/(r_c); % Pressao capilar maxima
delta_p_plus(i)=rho_l(i)*g*cosd(psi)*(r_v*2);% Pressao hidrostatica
delta_p_par(i)=rho_l(i)*g*sind(psi)*l; % Pressao hidrostatica
pe_b(i)=pc_max(i)-delta_p_plus(i)-delta_p_par(i)-delta_p_f; %Pressao efetiva de bombeamento
f_l(i)=((nu_l(i))/(k*a_w*hlv(i)*rho_l(i))); % Fator de atrito do liquido no meio poroso
f_v(i)=((cf*f_re*nu_v(i))/(2*((r_h_v)^2)*a_v*rho_v(i)*hlv(i))); % Fator de atrito do vapor % Para Re<2300 e Ma_v<0.2
 end

for i=1:n 
q_cap(i)=(pe_b(i))/((f_l(i)+f_v(i))*lef); %Q_capilar
q_capf(i)=((pc_max(i)-(rho_l(i)*g*l*sind(psi)))/(f_l(i)+f_v(i)));%/(1000);%Q_capilar livro de Faghri, pag 227
end

# sonic limit
for i in range(len(temperature)):
    rho_steam = PropsSI("D", "T", temperature[i], "Q", 1, fluid)
    enthalpy_liquid = PropsSI("H", "T", temperature[i], "Q", 0, fluid)
    enthalpy_steam = PropsSI("H", "T", temperature[i], "Q", 1, fluid)
    enthalpy_evaporation = enthalpy_steam - enthalpy_liquid
    specific_heat_pressure = PropsSI("C", "T", temperature[i], "Q", 1, fluid)
    specific_heat_volume = PropsSI("O", "T", temperature[i], "Q", 1, fluid)
    gamma_steam = specific_heat_pressure / specific_heat_volume
    molar_mass = PropsSI(fluid, "molemass")
    R_steam = R / molar_mass
    temperature_operation = temperature[i] # K
    rho_steam = PropsSI("D", "T", temperature[i], "Q", 1, fluid)

    max_sonic_heat = area_steam * rho_steam * enthalpy_evaporation * ( (gamma_steam * R_steam * temperature_operation)/(2*gamma_steam+2) )**0.5
    #q_s(i)=((a_v*rho_v(i)*hlv(i))*(((gamma*rv*T_t(i))/(2*(gamma+1)))^(0.5)));%/(1000);%%temperatura es en K

# Boiling limit
for i in range(len(temperature)):
    epsilon = 1 - (crimp_factor * pi * mesh_number * wire_diameter / 4)
    conductivity_liquid = PropsSI("L", "T", temperature[i], "Q", 0, fluid)
    conductivity_steam = PropsSI("L", "T", temperature[i], "Q", 1, fluid)
    kl = conductivity_liquid
    kw = conductivity_steam
    conductivity_effective = kl * ((kl+kw)-(1-epsilon)*(kl-kw)) / ( (kl+kw)+(1-epsilon)*(kl-kw) )
    sigma = PropsSI("I", "T", temperature[i], "Q", 0, fluid)
    temperature_operation = temperature[i] # K
    nucleation_critical_radius = 2.54E-5 # 2.54E-7 < rn < 2.54E-5 [m]
    radius_capilar = 1/(2*mesh_number)
    pressure_capilar = 2*sigma/radius_capilar

    enthalpy_liquid = PropsSI("H", "T", temperature[i], "Q", 0, fluid)
    enthalpy_steam = PropsSI("H", "T", temperature[i], "Q", 1, fluid)
    enthalpy_evaporation = enthalpy_steam - enthalpy_liquid
    rho_steam = PropsSI("D", "T", temperature[i], "Q", 1, fluid)

    max_boiling_heat = 2 * numpypi * length_evaporator * conductivity_effective * temperature_operation * (2*sigma/nucleation_critical_radius - pressure_capilar) / (enthapy_evaporation * rho_steam * numpy.log(radius_internal/radius_steam))
# q_e(i)=(((2*pi*le*keff(i)*T_t(i))/(hlv(i)*rho_v(i)*(log((0.5*d_int)/r_v))))*(((2*ts(i))/rn)-pc_max(i)));

# Drag limit
%% Limite do arrastro
r_h_w=(1/(2*N))-(d_f/2);

for i in range(len(temperature)):
    enthalpy_liquid = PropsSI("H", "T", temperature[i], "Q", 0, fluid)
    enthalpy_steam = PropsSI("H", "T", temperature[i], "Q", 1, fluid)
    enthalpy_evaporation = enthalpy_steam - enthalpy_liquid
    sigma = PropsSI("I", "T", temperature[i], "Q", 0, fluid)
    radius_hidraulic = 2 * area_steam / perimeter_steam

    max_drag_heat = area_steam * enthalpy_evaporation * (sigma*rho_steam/(2*radius_hidraulic))**(1/2)
    # q_em(i)=((a_v*hlv(i))*(((ts(i)*rho_v(i))/(2*r_h_w))^(0.5)));

# Viscous limit
for i in range(len(temperature)):
    enthalpy_liquid = PropsSI("H", "T", temperature[i], "Q", 0, fluid)
    enthalpy_steam = PropsSI("H", "T", temperature[i], "Q", 1, fluid)
    enthalpy_evaporation = enthalpy_steam - enthalpy_liquid
    rho_steam = PropsSI("D", "T", temperature[i], "Q", 1, fluid)
    pressure_steam = PropsSI("P", "T", temperature[i], "Q", 1, fluid)
    viscosity_steam = PropsSI("V", "T", temperature[i], "Q", 1, fluid)

    max_viscous_heat = (2*radius_steam)**2 * enthalpy_evaporation * rho_steam * pressure_steam / (64*viscosity_steam*length_effective)
    # q_v(i)=a_v*((((((2*r_v)^2)*hlv(i)*rho_v(i)*p0(i))/(64*nu_v(i)*lef))));

%% Plot limites de operacao
# plot
fig = plt.figure(1)
ax = fig.add_subplot(1,1,1)
# semilogy(tm,max_viscous_heat,'-rs','MarkerEdgeColor',[0 0 0],'MarkerSize',5,'MarkerFaceColor',[1 1 1])%Viscoso
ax.semilogy(temperature,max_capilar_heat,'-ks','MarkerEdgeColor',[0 0 0],'MarkerSize',5,'MarkerFaceColor',[0 0 0])
ax.semilogy(temperature,max_sonic_heat,'-ks','MarkerEdgeColor',[0 0 0],'MarkerSize',5,'MarkerFaceColor',[0.5 0.5 0.5])
ax.semilogy(temperature,max_boinling_heat,'-ks','MarkerEdgeColor',[0 0 0],'MarkerSize',5,'MarkerFaceColor',[1 1 1])
ax.semilogy(temperature,max_drag_heat,'-ko','MarkerEdgeColor',[0 0 0],'MarkerSize',5,'MarkerFaceColor',[1 1 1])
ax.semilogy(temperature,max_viscous_heat,'-k^','MarkerEdgeColor',[0 0 0],'MarkerSize',5,'MarkerFaceColor',[1 1 1])
# set(0,'DefaultAxesFontName', 'Times')
ax.grid(True)
ax.set_xlabel('Temperatura [\circC]','FontSize',12,'FontName','Times')
ax.set_ylabel('Q [W]','FontSize',12,'FontName','Times')
ax.set_legend('Capilar','Sonico','Ebulicao','Arrasto','Viscoso','Location','NorthWest')

plt.show()