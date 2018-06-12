"""

Nuevo formatea datos con troceador de archivo:

Pseudocódigo:


Pedimos la ruta del archivo
Comprobamos que el archivo exista y sea un csv
Generamos la carpeta en la que almacenamos los resultados
Generamos una carpeta auxiliar
Dividimos el archivo en x partes y lo almacenamos en la carpeta auxiliar
Almacenamos la ruta de los archivos en una lista
Procesamos cada uno de los archivos por separado, ojo que no pise el contenido de los anteriores
Borramos los archivos troceados y la carpeta auxiliar
Cerramos el archivo original


""" 


from contextlib import ExitStack
import math
from io import open
import os.path
import os
from pathlib import Path
from Modulos.Modulos import *
import shutil


print("Utilidad de formateo de datos. \n\n")

print("Para poder acceder a los datos de los diferentes medidores primero hay que procesar el archivo con los datos mensuales.")
print("Este archivo es el que podemos descargar del portal de Datos Abiertos.\n")
print("Para poder acceder al archivo te vamos a pedir la ruta de archivo, los datos resultantes se guardarán dentro de la carpeta en la que está el ejecutable, en Datos trafico.")
print("Mes Año son el mes y el año correspondiente a los datos\n")

print("Introduce la ruta completa en la que se encuentra el archivo. Este tiene que estar descomprimido y tener formato csv.")
print("Por ejemplo: D:\\Datos trafico\\09-2016.csv")
print("Si introduces la ruta de otro archivo csv existente que no sea de datos de tráfico de la página del Ayuntamiento el programa no funciona :D")
print("Si introduces la ruta de un archivo que no existe te la volverá a pedir. Buena suerte.\n")

#Pedimos la ruta del archivo y hacemos las comprobaciones que se puedan

pide_ruta=True

while(pide_ruta):
	ruta_archivo=input("Ruta del archivo -> ")
	if os.path.isfile(ruta_archivo):
		pide_ruta=False
	
	if (ruta_archivo[-4:]!=".csv"):
		print("Este archivo no es un csv :(")
		pide_ruta=True

anio=int(ruta_archivo[-8:-4])  #02-2018.csv
mes=int(ruta_archivo[-11:-9])

print("Año:", anio)
print("Mes: ", mes)

if(anio<2013 or anio>2018):
	print("Año fuera de rango :(")
	pide_ruta=True

if(mes<1 or mes>12):
	print("Ese mes no existe :(")
	pide_ruta=True

print("Ruta introducida: ", ruta_archivo)

print("\nEste proceso tarda un ratito. Puedes abrir la carpeta y ver cómo se generan los archivos. Es muy bonito.\n")

input("Pulsa enter para continuar.")


#Creamos la ruta de la carpeta en la que vamos a almacenar los resultados.

ruta_main=os.path.dirname(os.path.abspath(__file__))

ruta_carpeta=genera_ruta_carpeta(anio,mes,ruta_main) #nos devolverá "Directorio del main"\\Datos trafico\\mes_en_letra añoYYYY

if not os.path.exists(ruta_carpeta): #Comprueba la existencia de la carpeta y si no existe la crea.
	os.makedirs(ruta_carpeta)


#Generamos una carpeta auxiliar temp dentro de la carpeta de resultados
#OJO!!!, cambiar esto, para la prueba lo hacemos en la ruta archivo

ruta_carpeta_temp=ruta_archivo[:-11] + "temp\\" #le quitamos el nobre del archivo, los últimos 11 caracteres

print("Ruta archivo: ", ruta_archivo)
print("Ruta carpeta temporal: ", ruta_carpeta_temp)

try:
	os.makedirs(ruta_carpeta_temp)
except FileExistsError:
	next

#Ahora habría que llamar a la función splitcsv, convenientemente alojada en la librería que corresponda
#Vamos a probar a dividir el archivo en 8 partes

split_csv(ruta_archivo, ruta_carpeta_temp, 8)


#Almacenamos la ruta de los archivos en una lista

lista_archivos_temp=ls(ruta_carpeta_temp)


#Procesamos cada uno de los archivos por separado, ojo que no pise el contenido de los anteriores

for i in lista_archivos_temp:
	ruta_i=ruta_carpeta_temp+i #añadimos al nombre de archivo la ruta de la carpeta en la que se encuentra.
	print("Vamos a procesar el trozo: ", ruta_i)
	datos_i=open(ruta_i, "r")

	for j in datos_i:
		lista=j.split(";") #Transformamos cada linea del archivo en lista
		print("La lista que generamos con la linea del archivo es: ", lista)
						
		lista_fecha=separa_fechas(lista) #generamos una nueva lista con la fecha separada :)
		
		ruta_main=os.path.dirname(os.path.abspath(__file__))

		ruta_carpeta=genera_ruta_carpeta(lista_fecha[1],lista_fecha[2],ruta_main) #nos devolverá "Directorio del main"\\Datos trafico\\mes_en_letra añoYYYY
		if not os.path.exists(ruta_carpeta): #Comprueba la existencia de la carpeta y si no existe la crea.
			os.makedirs(ruta_carpeta)

		#ahora que tenemos en lista_fecha la fecha separada deberiamos generar la ruta del archivo [1]anio [2]mes [3]dia
		ruta_archivo=genera_ruta_archivo(lista_fecha[1], lista_fecha[2], lista_fecha[3], ruta_main) #"Directorio del main"\Datos trafico\Mes_en_letra YYYY\YYYY-MM-DD
		
		#Ahora que tenemos la ruta del archivo añadimos la línea correspondiente.
		
		resumen_diario=open(ruta_archivo, "a")
		resumen_diario.write("\n")
		resumen_diario.write(str(lista_fecha))
		resumen_diario.close()
	

	datos_i.close() 

#Borramos los archivos troceados y la carpeta auxiliar

shutil.rmtree(ruta_carpeta_temp)