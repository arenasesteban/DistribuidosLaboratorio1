from mpi4py import MPI

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

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if rank == 0:
        archivo_entrada = "archivos/archivo-entrada-20.txt"
        datos = leer_archivo(archivo_entrada)
        comm.send(datos, dest = 1)
    elif rank == 1:
        datos = comm.recv(source = 0)
        resultados = calcular_temperaturas(datos)
        comm.send(resultados, dest = 2) 
    else:
        resultados = comm.recv(source = 1)
        guardar_resultados(resultados, "archivos/archivo-salida-microservicios.txt")