%% Coisas que nao conhecemos:
% le, lad, lc
% c, b, cf, 
% kw (not used), rn (not used)

%% Calculo de tubos de calor
clear all
close all
clc
%% Informação conhecida
fluid='Methanol';
le=0.2; %Comprimento do evaporador [m]
lad=0.1; %Comprimento da secao adibatica [m]
lc=0.2; %Comprimento do condensador [m]

l=le+lad+lc; %Comprimento total [m]
q=80; %Calor dissipado [W]
psi=0;
xe=0:0.01:le; %Dominio do evaporador
xa=le:0.01:le+lad; %Dominio da seção adibatica
xc=le+lad:0.01:l; %Dominio do condensador
lef=(lc+le)/2+lad; %Comprimento efetivo [m]

%% Carateristicas do tubo de calor
d_f=28.06e-6; % Diametro do fio da tela [m]
d_ext=22.04e-3; %Diametro exterior do tubo [m]
t=0.9e-3; %Espessura do tubo [m]
c=10; %# de camadas
b=1; % Fator do coreção do momento
cf=1; %C fator de corecao  
f_re=16; % Fator de atrito de Faning laminar
S=1; %Fator de crimpagem professora recomendou
N=0.00768e+6; %Número de mesh
kw=100; % Conductividade térmica


r_v=(d_ext-2*t-(2*(c*d_f)))/2; %Raio do vapor [m]
a_v=pi*(r_v)^2; %Area do vapor  [m^2]
d_int=d_ext-2*t;
g=9.81; %Gravedade
T_ope=40;%Temperatura de operação [C]
%% Propriedades do fluido (Coolprop)
T_t=T_ope+273.15;%Temparetura de trabalho [K]

sigma=Props('I','T',T_t,'Q',1,fluid);%Tensão superficial [N/m^3]
r_efetivo = 1/(2*N);
rn=2*sigma/r_efetivo; %Pressao capilar da estrutura

%Pressao de saturacao [Pa]
p0=Props('P','T',T_t,'Q',1,fluid)*1000;
%Densidade do vapor [kg/m^3]
rho_v=Props('D','T',T_t,'Q',1,fluid);
%Densidade do liquido [kg/m^3]
rho_l=Props('D','T',T_t,'Q',0,fluid);
%Viscosidade do vapor [N-s/m^2]
nu_v=Props('V','T',T_t,'Q',1,fluid);
%Viscosidade do liquido [N-s/m^2]
nu_l=Props('V','T',T_t,'Q',0,fluid);
%Calor latente de vaporização [kJ/kg]
h_v=Props('H','T',T_t,'Q',1,fluid);
h_l=Props('H','T',T_t,'Q',0,fluid);
hlv=(h_v-h_l)*10^3;
%Tensão superficial [N/m^3]
ts=Props('I','T',T_t,'Q',1,fluid);
%C_P
c_p=Props('C','T',T_t,'P',p0,fluid);
%C_v
c_v=Props('O','T',T_t,'P',p0,fluid);
%Massa molar
mm=Props(fluid,'molemass');
%Conductividade termica do liquido
kl=Props('L','T',T_t,'Q',0,fluid)*1000;
%Conductividade termica do vapor
kv=Props('L','T',T_t,'Q',1,fluid)*1000;

gamma=1.33; % Vapor poliatomico
r=8.314e3; %Constante universal dos gases
rv=r/mm; %Constante do vapor

%% Fluxo mássico total
m_t=q/hlv;

 %% Pressão na fase vapor
%% Queda de pressão
delta_pe= ((-m_t*le)/2)*( ((f_re*nu_v)/(2*a_v*((r_v)^2)*rho_v))+((2*b*m_t)/( rho_v*((a_v)^2)*le))); %Evaporador
delta_pa=(-m_t*lad)*(((f_re*nu_v)/(2*a_v*((r_v)^2)*rho_v))); %Seção adibática
delta_pc=(-m_t*lc*0.5)*(((f_re*nu_v)/(2*a_v*((r_v)^2)*rho_v))-((2*b*m_t)/((rho_v)*((a_v)^2))*le)); %Condensador

%% Distribuição de pressão na fase vapor
pe=p0-(m_t/le)*(((f_re*nu_v)/(2*a_v*((r_v)^2)*rho_v)+((2*b*m_t)/(rho_v*(a_v^2)*le))))*(0.5*xe.^2); %Evaporador
pa=p0+delta_pe-m_t*((f_re*nu_v)/(2*a_v*((r_v)^2)*rho_v))*(xa-le); %Seção adibática
pc=p0+ delta_pe + delta_pa -(m_t/lc)*(((f_re*nu_v)/(2*a_v*(r_v^2)*rho_v))-((2*b*m_t)/(rho_v*(a_v^2)*le)))*(((xc.^2)/2)-l*xc-((le+lad).^2/2)+ l*(le+lad)); %Condensador

%Plot distribuição de pressão
fig_2 = figure(2);
grid on
grid on
hold on
box on
plot(xe,pe,'k','LineWidth',1)
plot(xa,pa,'k','LineWidth',1)
plot(xc,pc,'k','LineWidth',1)
set(0,'DefaultAxesFontName', 'Times')
xlabel('Comprimento x[m] ','FontSize',12,'FontName','Times')
ylabel('Pressão [Pa]','FontSize',12,'FontName','Times')
title(strcat('Pressão do vapor no tubo ao longo do comprimento - ',fluid))
saveas(fig_2, strcat('steam_',fluid,'.png'));
%Queda total de pressão no vapor
delta_v=delta_pe+delta_pa+delta_pc;

%% Pressão na fase líquida
%% Meio poroso
epsilon=1-((S*pi*N*d_f)/(4));
k=(((d_f)^2)*(epsilon^3))/(122*((1-epsilon)^2)); %Permeabilidade
a_w=(pi/4)*((d_ext-2*t)^2-(2*r_v)^2); %Area do liquido
%% Queda de pressão
delta_pl_e=((nu_l*m_t*le )/(2*rho_l*k*a_w)); %Evaporador delta_pe_e
delta_pl_a=((nu_l*m_t*lad)/(rho_l*k*a_w)); %Seção adibática
delta_pl_c=((nu_l*m_t*lc)/(2*rho_l*k*a_w)); %Condensador
%% Distribuição de pressão na fase líquida
pc_l=p0 - delta_pc - delta_pl_c + ((nu_l*m_t)/(rho_l*k*a_w*lc))*((-xc.^2/2)+((le+lad).^2/2)+l*xc-l*(le+lad));
pa_l=p0 - delta_pl_a - delta_pc - delta_pl_c + ((nu_l*m_t)/(rho_l*k*a_w))*(xa-le);
pe_l=p0 - delta_pl_e - delta_pl_a - delta_pc - delta_pl_c +((nu_l*m_t)/(2*rho_l*k*a_w*le))*(xe.^2);

%Plot distribuição de pressão
fig_3 = figure(3);
grid on
hold on
box on
plot(xe,pe_l,'k','LineWidth',1)
plot(xa,pa_l,'k','LineWidth',1)
plot(xc,pc_l,'k','LineWidth',1)
set(0,'DefaultAxesFontName', 'Times')
xlabel('Comprimento x[m] ','FontSize',12,'FontName','Times')
ylabel('Pressão [Pa]','FontSize',12,'FontName','Times')
title(strcat('Pressão do líquido no tubo ao longo do comprimento - ',fluid))
saveas(fig_3, strcat('liquid_',fluid,'.png'));