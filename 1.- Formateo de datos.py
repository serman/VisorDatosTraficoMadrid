"""

Nuevo formatea datos adaptando el archivo de salida a la cabecera de entrada:

Pseudocódigo:


Pedimos la ruta del archivo
Comprobamos que el archivo exista y sea un csv
Lo que vamos a hacer aquí es leer la primera línea de un archivo de datos de tráfico y ver qué campos tenemos
que dejar para que cada línea de salida sea de la siguiente manera:

"idelem"; "fecha";               "tipo_elem";          "intensidad"; "ocupacion"; "carga"; "vmed"; "error"; "periodo_integracion"
6900;     "2017-01-01 01:00:00"; "PUNTOS MEDIDA M-30"; 168;          1;           0;       49;     "N";     5

[0]idelem 					string
[1]fecha 					string
[2]tipo_elem	 			string
[3]intensidad 				int
[4]ocupacion 				int
[5]carga 					int
[6]vmed  					int
[7]error 					string
[8]periodo_integracion 		int

Para ello:

Aplicamos el método split a la línea.

Encontramos los índices de los campos que queremos que tenga nuestra línea resultado

Formamos la línea resultado

Escribimos la línea en el archivo de salida.
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

print() #Línea en blanco
print(f"El archivo debería corresponder al mes {mes} del año {anio}.")

if(anio<2013 or anio>2018):
	print("Año fuera de rango :(")
	pide_ruta=True

if(mes<1 or mes>12):
	print("Ese mes no existe :(")
	pide_ruta=True



print("\nEste proceso tarda un ratito. Puedes abrir la carpeta y ver cómo se generan los archivos. Es muy bonito.\n")

input("Pulsa enter para continuar.")


#Creamos la ruta de la carpeta en la que vamos a almacenar los resultados.

ruta_main=os.path.dirname(os.path.abspath(__file__))

ruta_carpeta=genera_ruta_carpeta(anio,mes,ruta_main) #nos devolverá "Directorio del main"\\Datos trafico\\mes_en_letra añoYYYY

if not os.path.exists(ruta_carpeta): #Comprueba la existencia de la carpeta y si no existe la crea.
	os.makedirs(ruta_carpeta)


#Procesamos el archivo de datos adaptando cada línea según la cabecera.

datos=open(ruta_archivo, "r")

primera_linea=True

for i in datos:
	lista_i=i.split(";")
	if (primera_linea): #estamos en la primera línea del archivo
		try:
			indice_idelem=lista_i.index("\"idelem\"")
		except ValueError:
			indice_idelem=lista_i.index("\"id\"")

		indice_fecha=lista_i.index("\"fecha\"")

		indice_tipo_elem=lista_i.index("\"tipo_elem\"")

		indice_intensidad=lista_i.index("\"intensidad\"")

		indice_ocupacion=lista_i.index("\"ocupacion\"")

		indice_carga=lista_i.index("\"carga\"")

		indice_vmed=lista_i.index("\"vmed\"")

		indice_error=lista_i.index("\"error\"")

		indice_periodo=lista_i.index("\"periodo_integracion\"\n") #el \n es por ser el último de la linea

		#ya tenemos los índices en los que aparecen los datos que queremos, de modo que pasamos ya a la línea de datos
		primera_linea=False
		continue

	#Formamos la lista con los datos que queremos en el orden que queremos.
	lista_resultado=[lista_i[indice_idelem],lista_i[indice_fecha],lista_i[indice_tipo_elem],lista_i[indice_intensidad],lista_i[indice_ocupacion],lista_i[indice_carga],lista_i[indice_vmed],lista_i[indice_error],lista_i[indice_periodo]]

	#Generamos la lista con los datos de la fecha separados.
	lista_fecha=separa_fechas(lista_resultado) 

	#Nos devuelve "Directorio del main"\\Datos trafico\\mes_en_letra añoYYYY
	ruta_carpeta=genera_ruta_carpeta(lista_fecha[1],lista_fecha[2],ruta_main)

	#Comprueba la existencia de la carpeta y si no existe la crea.
	if not os.path.exists(ruta_carpeta): 
		os.makedirs(ruta_carpeta)

	#Ahora que tenemos en lista_fecha la fecha separada generamos la ruta del archivo [1]anio [2]mes [3]dia
	ruta_archivo=genera_ruta_archivo(lista_fecha[1], lista_fecha[2], lista_fecha[3], ruta_main) #"Directorio del main"\Datos trafico\Mes_en_letra YYYY\YYYY-MM-DD

	#Con la ruta del archivo añadimos la línea correspondiente.
	resumen_diario=open(ruta_archivo, "a")
	resumen_diario.write(str(lista_fecha)+"\n")
	resumen_diario.close()

datos_i.close() 



"""

from io import open

datos=open("D:\\Datos trafico\\01-2018.csv", "r")

contador=0

for i in datos:
	lista_i=i.split(";")
	if (contador==0): #estamos en la primera línea del archivo
		try:
			indice_idelem=lista_i.index("\"idelem\"")
		except ValueError:
			indice_idelem=lista_i.index("\"id\"")
		print("Idelem aparece en la posición ", indice_idelem)

		indice_fecha=lista_i.index("\"fecha\"")
		print("Fecha aparece en la posición ", indice_fecha)

		indice_tipo_elem=lista_i.index("\"tipo_elem\"")
		print("Tipo_elem aparece en la posición ", indice_tipo_elem)

		indice_intensidad=lista_i.index("\"intensidad\"")
		print("Intensidad aparece en la posición ", indice_intensidad)

		indice_ocupacion=lista_i.index("\"ocupacion\"")
		print("Ocupacion aparece en la posición ", indice_ocupacion)

		indice_carga=lista_i.index("\"carga\"")
		print("carga aparece en la posición ", indice_carga)

		indice_vmed=lista_i.index("\"vmed\"")
		print("vmed aparece en la posición ", indice_vmed)

		indice_error=lista_i.index("\"error\"")
		print("Error aparece en la posición ", indice_error)

		indice_periodo=lista_i.index("\"periodo_integracion\"\n") #el \n es por ser el último de la linea
		print("periodo aparece en la posición ", indice_periodo)

	
	lista_resultado=[lista_i[indice_idelem],lista_i[indice_fecha],lista_i[indice_tipo_elem],lista_i[indice_intensidad],lista_i[indice_ocupacion],lista_i[indice_carga],lista_i[indice_vmed],lista_i[indice_error],lista_i[indice_periodo]]


	print("\nLa línea tal cual se lee del archivo", i)
	print("La línea transformada en lista: ", lista_i,"\n")
	print("Longitud de la lista:", len(lista_i),"\n")
	print("La lista resultado, siempre con el mismo formato: \n", lista_resultado)

	resumen_diario=open("D:\\Datos trafico\\resultado.csv", "a")
	resumen_diario.write("\n")
	resumen_diario.write(str(lista_resultado))
	resumen_diario.close()



	#Break para no recorrer todo el archivo
	contador+=1
	if contador>=3:
		break

datos.close()


"""