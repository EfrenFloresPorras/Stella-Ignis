import serial
import csv
import matplotlib.pyplot as plt

# Configura el puerto serial
ser = serial.Serial('COM3', baudrate=57600)  # Reemplaza 'COMX' con el puerto serial de tu Arduino

# Inicializa listas para almacenar datos
x_data, y_data = [], []

# Configura la figura y los ejes
plt.ion()
fig, ax = plt.subplots()
line, = ax.plot(x_data, y_data)

# Abre el archivo CSV para escribir los datos
with open('datos.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Número', 'Valor de Fuerza'])

    # Configura el bucle principal
    while True:
        try:
            # Lee el valor de fuerza desde el puerto serial
            force = float(ser.readline().decode('utf-8').rstrip())

            # Guarda los datos en el archivo CSV
            csvwriter.writerow([len(x_data) + 1, force])

            # Actualiza los datos
            x_data.append(len(x_data) + 1)  # Para contar los datos recibidos
            y_data.append(force)

            # Actualiza la línea en el gráfico
            line.set_xdata(x_data)
            line.set_ydata(y_data)

            # Ajusta los límites de los ejes
            ax.relim()
            ax.autoscale_view()

            # Redibuja el gráfico
            plt.draw()
            plt.pause(0.01)

        except KeyboardInterrupt:
            break

# Cierra el puerto serial
ser.close()
