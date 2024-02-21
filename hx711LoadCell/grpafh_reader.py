import csv
import matplotlib.pyplot as plt

# Estilo y colores personalizados
plt.style.use('seaborn-darkgrid')
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=['red', 'black'])

# Listas para almacenar los datos
x_data = []
y_data = []

# Lee el archivo CSV
with open('datos.csv', 'r') as csvfile:
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        x_data.append(float(row['numero']))
        y_data.append(float(row['valor de fuerza']))

# Grafica los datos
plt.plot(x_data, y_data)
plt.xlabel('Número')
plt.ylabel('Valor de Fuerza')
plt.title('Gráfico de Datos')
plt.grid(True)
plt.show()
