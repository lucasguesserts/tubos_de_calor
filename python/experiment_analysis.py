import csv

path = "../dados_experimentos/experimento_tubos_de_calor_01.txt"
file = open(path, newline="", encoding="utf16")
csv_file = csv.reader(file, delimiter="\t")
header = next(csv_file)
data = []
for row in csv_file:
   iteration = int(row[0]) 
   power = float(row[1])
   evaporator_1 = float(row[2])
   evaporator_2 = float(row[3])
   evaporator_3 = float(row[4])
   evaporator_4 = float(row[5])
   adiabatic_1 = float(row[6])
   adiabatic_2 = float(row[7])
   condenser_1 = float(row[8])
   condenser_2 = float(row[9])
   condenser_3 = float(row[10])
   condenser_4 = float(row[11])
   environment = float(row[12])
   data.append([evaporator_1, evaporator_2, evaporator_3, evaporator_4, adiabatic_1, adiabatic_2, condenser_1, condenser_2, condenser_3, condenser_4, environment])

print(data)
