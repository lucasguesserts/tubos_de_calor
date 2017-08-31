%% Calculo de tubos de calor
clear all
close all
clc
%% Informação conhecida
le=0.3; %Comprimento do evaporador [m]
lad=0.1; %Comprimento da secao adibatica [m]
lc=0.5; %Comprimento do condensador [m]
l=le+lad+lc; %Comprimento total [m]
q=30; %Calor dissipado [W]
psi=-90;
xe=0:0.01:le; %Dominio do evaporador
xa=le:0.01:le+lad; %Dominio da seção adibatica
xc=le+lad:0.01:l; %Dominio do condensador
lef=(lc+le)/2+lad; %Comprimento efetivo [m]

%% Carateristicas do tubo de calor
d_f=1.143e-4; % Diametro do fio da tela [m]
d_ext=31.75e-3; %Diametro exterior do tubo [m]
t=3.17e-3; %Espessura do tubo [m]
c=10; %# de camadas
b=1; % Fator do coreção do momento
cf=1; %C fator de corecao  
f_re=16; % Fator de atrito de Faning laminar
S=1.05; %Fator de crimpagem (Chi,1975)
N=100/0.0254; %Número de mesh
% r_v=(d_ext-2*t-(2*(c*d_f)))/2; %Raio do vapor [m]
esp=1;
r_v=(d_ext-2*t-(esp*2*(c*d_f)))/2; %Raio do vapor [m]
a_v=pi*(r_v)^2; %Area do vapor  [m^2]
d_int=d_ext-2*t;
g=9.81; %Gravedad
kw=237;
rn=2.54e-7; %Pressao capilar da estrutura
T_ope=40;%Temperatura de operação [C]
t_min=-20;
t_max=100;
n=25;
tm=linspace(t_min,t_max,n);% Con n=23, espacamento=5 C na temperatura
fluid='Acetone';

%% Propiedades do fluido (Coolprop)
%Acetona
for i=1:n %Temparetura de trabalho [K]
 T_t(i)=tm(i)+273.15;   
 p0(i)=Props('P','T',T_t(i),'Q',1,fluid)*1000;  
 rho_v(i)=Props('D','T',T_t(i),'Q',1,'Acetone');
 rho_l(i)=Props('D','T',T_t(i),'Q',0,'Acetone');
 nu_v(i)=Props('V','T',T_t(i),'Q',1,'Acetone');
 nu_l(i)=Props('V','T',T_t(i),'Q',0,'Acetone');
 h_v(i)=Props('H','T',T_t(i),'Q',1,'Acetone');
 h_l(i)=Props('H','T',T_t(i),'Q',0,'Acetone');
 ts(i)=Props('I','T',T_t(i),'Q',1,'Acetone');
 c_p(i)=Props('C','T',T_t(i),'P',p0,'Acetone');
 hlv(i)=(h_v(i)-h_l(i))*10^3;
 c_v(i)=Props('O','T',T_t(i),'P',p0,'Acetone');
 kl(i)=Props('L','T',T_t(i),'Q',0,'Acetone')*1000;
 kv(i)=Props('L','T',T_t(i),'Q',1,'Acetone')*1000;
end
% T_t=T_ope+273.15;%Temparetura de trabalho [K]

gamma=1.33; % Vapor poliatomico
r=8.314e3; %Constante universal dos gases
mm=Props('Acetone','molemass'); % Massa molar
rv=r/mm; %Constante do vapor

epsilon=1-((S*pi*N*d_f)/(4));
k=(((d_f)^2)*(epsilon^3))/(122*((1-epsilon)^2)); %Permeabilidade
a_w=(pi/4)*((d_ext-2*t)^2-(2*r_v)^2); %Area do liquido
 
%% Limites de operacao
%% Limite capilar
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


%% Limite sonico
for i=1:n 
q_s(i)=((a_v*rho_v(i)*hlv(i))*(((gamma*rv*T_t(i))/(2*(gamma+1)))^(0.5)));%/(1000);%%temperatura es en K
re_v(i)=(2*r_v*q)/(a_v*nu_v(i)*hlv(i));
ma_v(i)=(q)/((a_v*rho_v(i)*hlv(i)*((rv*T_t(i)*gamma)^(0.5)))); % Mach
end

%% Limite ebilucao
for i=1:n 
keff(i)=(kl(i)*(kl(i)+kw-(1-epsilon)*(kl(i)-kw)))/(kl(i)+kw+(1-epsilon)*(kl(i)-kw)); %Conductividade efetiva do meio poroso
q_e(i)=(((2*pi*le*keff(i)*T_t(i))/(hlv(i)*rho_v(i)*(log((0.5*d_int)/r_v))))*(((2*ts(i))/rn)-pc_max(i)));
end


%% Limite do arrastro
r_h_w=(1/(2*N))-(d_f/2);

for i=1:n 
q_em(i)=((a_v*hlv(i))*(((ts(i)*rho_v(i))/(2*r_h_w))^(0.5)));
end

%% Limite viscoso
for i=1:n 
q_v(i)=a_v*((((((2*r_v)^2)*hlv(i)*rho_v(i)*p0(i))/(64*nu_v(i)*lef))));
end

%% Plot limites de operacao
figure(4)
box on
% semilogy(tm,q_cap,'-rs','MarkerEdgeColor',[0 0 0],'MarkerSize',5,'MarkerFaceColor',[1 1 1])%Viscoso
semilogy(tm,q_capf,'-ks','MarkerEdgeColor',[0 0 0],'MarkerSize',5,'MarkerFaceColor',[0 0 0])%Capilar
hold on
semilogy(tm,q_s,'-ks','MarkerEdgeColor',[0 0 0],'MarkerSize',5,'MarkerFaceColor',[0.5 0.5 0.5])%Sonico
semilogy(tm,q_e,'-ks','MarkerEdgeColor',[0 0 0],'MarkerSize',5,'MarkerFaceColor',[1 1 1])%Ebilucao
semilogy(tm,q_em,'-ko','MarkerEdgeColor',[0 0 0],'MarkerSize',5,'MarkerFaceColor',[1 1 1])%Arrastro
semilogy(tm,q_v,'-k^','MarkerEdgeColor',[0 0 0],'MarkerSize',5,'MarkerFaceColor',[1 1 1])%Viscoso
set(0,'DefaultAxesFontName', 'Times')
grid on
xlabel('Temperatura [\circC]','FontSize',12,'FontName','Times')
ylabel('Q [W]','FontSize',12,'FontName','Times')
legend('Capilar','Sônico','Ebulição','Arrasto','Viscoso','Location','NorthWest');
