import csv
import matplotlib.pyplot as plt
plt.rc('text', usetex=True)

# path = "../dados_experimentos/experimento_tubos_de_calor_01.txt"
# file = open(path, newline="", encoding="utf8")
# csv_file = csv.reader(file, delimiter="\t")
# header = next(csv_file)
# temperatures = {}
# for row in csv_file:
   # iteration = int(float(row[0].replace(",",".")))
   # power = float(row[1].replace(",","."))
   # evaporator_1 = float(row[2].replace(",","."))
   # evaporator_2 = float(row[3].replace(",","."))
   # evaporator_3 = float(row[4].replace(",","."))
   # evaporator_4 = float(row[5].replace(",","."))
   # adiabatic_1 = float(row[6].replace(",","."))
   # adiabatic_2 = float(row[7].replace(",","."))
   # condenser_1 = float(row[8].replace(",","."))
   # condenser_2 = float(row[9].replace(",","."))
   # condenser_3 = float(row[10].replace(",","."))
   # condenser_4 = float(row[11].replace(",","."))
   # environment = float(row[12].replace(",","."))
   # # temperatures.append([evaporator_1, evaporator_2, evaporator_3, evaporator_4, adiabatic_1, adiabatic_2, condenser_1, condenser_2, condenser_3, condenser_4, environment])
   # temperatures[iteration] = ([evaporator_1, evaporator_2, evaporator_3, evaporator_4, adiabatic_1, adiabatic_2, condenser_1, condenser_2, condenser_3, condenser_4, environment])

# print(temperatures[525])
# print(temperatures[524])

path = "../dados_experimentos/experimentos.csv"
file = open(path, newline="")
csv_file = csv.reader(file)

header = next(csv_file)

data = []
for row in csv_file:
    experiment = int(row[0])
    inclination = float(row[1])
    power = float(row[2])
    evaporator_1 = float(row[3])
    evaporator_2 = float(row[4])
    evaporator_3 = float(row[5])
    evaporator_4 = float(row[6])
    adiabatic_1 = float(row[7])
    adiabatic_2 = float(row[8])
    condenser_1 = float(row[9])
    condenser_2 = float(row[10])
    condenser_3 = float(row[11])
    condenser_4 = float(row[12])
    environment = float(row[13])
    fluid = str(row[14])
    fluid_quantity = float(row[15])
    convection_type = str(row[16])
    air_velocity = float(row[17])
    adiabatic_section_removed_length = float(row[18])

    data.append([experiment, inclination, power, evaporator_1, evaporator_2, evaporator_3, evaporator_4, adiabatic_1, adiabatic_2, condenser_1, condenser_2, condenser_3, condenser_4, environment, fluid, fluid_quantity, convection_type, air_velocity, adiabatic_section_removed_length])

# for i in range(len(data)):
    # print(data[i])

# data of each experiment
experiment_simple_data = []
powers = []
for i in range(len(data)):
    experiment_simple_data.append([data[i][j] for j in range(3, 13)])

# for row in experiment_simple_data:
    # print(row)
positions = [40, 80, 120, 160, 233, 266, 340, 380, 420, 460]
for i in range(len(data)):
    fig_size = 8
    figFontSize = 14
    fig = plt.figure(i, figsize=((1/0.7)*fig_size,fig_size))
    ax = fig.add_subplot(111)
    ax.plot(positions, experiment_simple_data[i], "-ks")
    ax.grid(True)
# Experiment description
    experiment_info = r"Experimento {}:\\\\".format(data[i][0])
    power_info = r"Pot\^encia: {:2.0f} [$W$]\\\\".format(data[i][2])
    inclination_info = r"Inclina\c c\~ao: {:2.0f} [$graus$]\\\\".format(data[i][1])
    fluid_info = r"Fluido: {:2.1f} $ml$ de {:s}\\\\".format(data[i][15], data[i][14])
    refrigeration_info = r"Refrigera\c c\~ao: convec\c c\~ao {:s}\\\\".format(data[i][16])
    air_velocity_info = r"Velocidade do ar: {:2.1f} [$m/s$]\\\\".format(data[i][17])
    adiabatic_info = r"Comprimento da se\c c\~ao\\adiab\'atica removido: {:2.0f} [$mm$]".format(1000*data[i][18])
    description = experiment_info + power_info + inclination_info + fluid_info + refrigeration_info + air_velocity_info + adiabatic_info
# figure insert information
    figure_name = r"images/experiment_{}_power_{:2.0f}.png".format(data[i][0], data[i][2])
    text_title = r"Distribui\c c\~ao de temperatura no\\tubo de calor em fun\c c\~ao do comprimento"
    text_xlabel = r"Comprimento [$mm$]"
    text_ylabel = r"Temperatura [$C$]"
    ax.set_title(text_title, multialignment="center")
    ax.set_xlabel(text_xlabel, fontsize=figFontSize)
    ax.set_ylabel(text_ylabel, fontsize=figFontSize)
    fig.text(0.72, 0.4, description, fontsize=figFontSize)
    fig.subplots_adjust(right=0.7)
    fig.savefig(figure_name)
