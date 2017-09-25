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

positions = [40, 80, 120, 160, 233, 266, 340, 380, 420, 460]
