# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 13:49:08 2024

@author: bryan
"""

from mpi4py import MPI

arreglo = {}

# Función para procesar una línea del archivo
def procesar_linea(linea):
    estacion, temperatura = linea.split(';')
    return estacion, float(temperatura)


if __name__ == '__main__':
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    if rank == 0:  # Proceso principal
        archivo = 'datos.txt'
        with open(archivo, 'r') as f:
            lineas = f.readlines()
        

        for linea in lineas:
            estacion, temperatura = procesar_linea(linea)

            if estacion not in arreglo:
                # Se guarda en el arreglo la nueva estación leída
                arreglo[estacion] = [temperatura, temperatura, temperatura, 1]
            else:
                # Envío de datos a proceso 1 y proceso 2
                comm.send((estacion, temperatura), dest=1)
                comm.send((estacion, temperatura), dest=2)

                # Esperar a que proceso 1 y proceso 2 terminen
                comm.recv(source=1)
                comm.recv(source=2)
        
        # Se envía un mensaje de finalización a los procesos 1 y 2
        comm.send(('FIN', temperatura), dest=1)
        comm.send(('FIN', temperatura), dest=2)    

        print("Arreglo final:", arreglo)

    elif rank == 1:  # Proceso 1
        while True:
            estacion, temperatura = comm.recv(source=0)
            if estacion == 'FIN':
                break
            # Se comprueba si la nueva temperatura es un maximo 
            if temperatura > arreglo[estacion][0]:
                arreglo[estacion][0] = temperatura # Se guarda
            # Se comprueba si la nueva temperatura es un minimo
            elif temperatura < arreglo[estacion][1]:
                arreglo[estacion][1] = temperatura # Se guarda
                
            comm.send(None, dest=0)

    elif rank == 2:  # Proceso 2
        while True:
            estacion, temperatura = comm.recv(source=0)
            if estacion == 'FIN':
                break
            # Se revierte el promedio para obtener la suma de las temperaturas
            suma = arreglo[estacion][2] * arreglo[estacion][3] 
            # Se suma la nueva temperatura
            suma = suma + temperatura
            # Se guarda el nuevo promedio
            arreglo[estacion][2] = suma / (arreglo[estacion][3] + 1)
            # Se guarda el nuevo valor de contador
            arreglo[estacion][3] = arreglo[estacion][3] + 1
        comm.send(None, dest=0)
