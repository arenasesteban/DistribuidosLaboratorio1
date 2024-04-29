from mpi4py import MPI
import tkinter as tk
import time

ini_time = 0.0
fin_time = 0.0


# Definir una constante para la señal de fin de transmisión
FIN_TRANSMISION = "FIN"

def leer_archivo(archivo, rank_destino, comm):
    with open(archivo, 'r') as file:
        for linea in file:
            estacion, temperatura = linea.split(';')
            comm.send((estacion, float(temperatura)), dest = rank_destino)
    comm.send(FIN_TRANSMISION, dest = rank_destino)

def calcular_temperaturas(rank_origen, rank_destino, comm):
    comm = MPI.COMM_WORLD
    estaciones = []

    while True:
        data = comm.recv(source = rank_origen)
        
        if data == FIN_TRANSMISION:
            break

        estacion, temperatura = data

        for datos_estacion in estaciones:
            if datos_estacion[0] == estacion:
                datos_estacion[1] = min(datos_estacion[1], temperatura)
                datos_estacion[2] = max(datos_estacion[2], temperatura)
                datos_estacion[3] += temperatura
                datos_estacion[4] += 1
                break
        else:
            estaciones.append([estacion, temperatura, temperatura, temperatura, 1])
        
    for datos_estacion in estaciones:
        comm.send(datos_estacion, dest = rank_destino)
    comm.send(FIN_TRANSMISION, dest = rank_destino)

def guardar_resultados(rank_origen, archivo_salida, comm):
    resultados = []

    while True:
        data = comm.recv(source = rank_origen)
 
        if data == FIN_TRANSMISION:
            break

        resultados.append(data)
    
    with open(archivo_salida, 'w') as file:
        file.write("Estacion;Temp. Minima;Temp. Maxima;Temp. Promedio\n")


        for estacion, temp_min, temp_max, temp_total, contador in resultados:
            temp_promedio = temp_total / contador
            file.write(f"{estacion};{temp_min};{temp_max};{temp_promedio:.1f}\n")
            etiqueta_resultado = tk.Label(ventana, text=f"Estación: {estacion} - Temp. Mínima: {temp_min} - Temp. Máxima: {temp_max} - Temp. Promedio: {temp_promedio:.1f}")
            etiqueta_resultado.pack()
        

def interfaz():
    guardar_resultados(1, archivo_salida, comm)

def deshabilitar_boton():
    boton.config(state="disabled")

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if rank == 0:
        ini_time= time.time()
        print(ini_time)
        archivo_entrada = "archivos/archivo-entrada-20.txt"
        leer_archivo(archivo_entrada, 1, comm)
    elif rank == 1:
        calcular_temperaturas(0, 2, comm)
        fin_time = time.time()
        print(fin_time)
    else:
        archivo_salida = "archivos/archivo-salida-eventos.txt"
        # Crear la ventana
        ventana = tk.Tk()
        ventana.title("Arquitectura eventos")
        ventana.geometry("400x300")  # Tamaño de la ventana

        # Crear un botón que ejecutará la función al ser presionado
        boton = tk.Button(ventana, text="Presionar para ejecutar", command=lambda: [interfaz(), deshabilitar_boton()])
        boton.pack()

        # Ejecutar el bucle principal
        ventana.mainloop()
        

    