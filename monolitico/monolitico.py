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

archivo_entrada = "archivos/archivo-entrada-20.txt"
datos = leer_archivo(archivo_entrada)
resultados = calcular_temperaturas(datos)

for estacion, temp_min, temp_max, temp_promedio in resultados:
    print(f"Estación: {estacion} - Temp. Mínima: {temp_min} - Temp. Máxima: {temp_max} - Temp. Promedio: {temp_promedio:.1f}")