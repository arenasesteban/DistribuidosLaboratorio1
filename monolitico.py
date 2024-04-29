import tkinter as tk
import time

ini_time = 0.0
fin_time = 0.0


def leer_archivo(archivo):
    datos = []
    with open(archivo, 'r') as file:
        for linea in file:
            estacion, temperatura = linea.split(';')
            datos.append((estacion, float(temperatura)))
    return datos

def calcular_temperaturas(datos):
    estaciones = []
    resultados = []

    for estacion, temperatura in datos:
        if estacion not in estaciones:
            estaciones.append(estacion)

            temp_min = temperatura
            temp_max = temperatura
            temp_total = 0
            temp_contador = 0

            for estacion_aux, temp_aux in datos:
                if estacion_aux == estacion:
                    temp_min = min(temp_min, temp_aux)
                    temp_max = max(temp_max, temp_aux)
                    temp_total += temp_aux
                    temp_contador += 1

            temp_promedio = temp_total / temp_contador
            resultados.append((estacion, temp_min, temp_max, temp_promedio))
            
    return resultados

def guardar_resultados(resultados, archivo_salida):
    with open(archivo_salida, 'w') as file:
        file.write("Estacion;Temp. Minima;Temp. Maxima;Temp. Promedio\n")
        for estacion, temp_min, temp_max, temp_promedio in resultados:
            file.write(f"{estacion};{temp_min};{temp_max};{temp_promedio:.1f}\n")

def monolitico():
    ini_time = time.time()
    archivo_entrada = "archivos/archivo-entrada-1000.txt"
    datos = leer_archivo(archivo_entrada)
    resultados = calcular_temperaturas(datos)
    fin_time = time.time()
    print(ini_time)
    print(fin_time)

    guardar_resultados(resultados, "archivos/archivo-salida-monolitico.txt")
    

    for estacion, temp_min, temp_max, temp_promedio in resultados:
        etiqueta_resultado = tk.Label(ventana, text=f"Estación: {estacion} - Temp. Mínima: {temp_min} - Temp. Máxima: {temp_max} - Temp. Promedio: {temp_promedio:.1f}")
        etiqueta_resultado.pack()


# Crear la ventana
ventana = tk.Tk()
ventana.title("Arquitectura monolitica")
ventana.geometry("400x300")  # Tamaño de la ventana



# Crear un botón que ejecutará la función al ser presionado
boton = tk.Button(ventana, text="Presionar para ejecutar", command=monolitico)
boton.pack()

# Ejecutar el bucle principal
ventana.mainloop()