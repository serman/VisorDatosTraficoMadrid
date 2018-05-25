"""

Esto es hacer bien el programa 5.-Resumen diario

Pedimos el mes y el año
Generamos la ruta
Comprobamos que está el archivo
Extraemos los datos diarios

"""

from io import open
from Main.Modulos import *
import os.path
import os

print("Utilidad de formateo de datos. \n\n")

print("Para poder acceder a los datos de los diferentes medidores primero hay que procesar el archivo con los datos mensuales.")
print("Este archivo es el que podemos descargar del portal de Datos Abiertos.\n")
print("Para poder acceder al archivo te vamos a pedir la ruta de archivo, los datos resultantes se guardarán dentro de la carpeta en la que está el ejecutable, en Datos trafico.")
print("Mes Año son el mes y el año correspondiente a los datos\n")

print("Introduce la ruta completa en la que se encuentra el archivo. Este tiene que estar descomprimido y tener formato csv.")
print("Utiliza los separadores \\ en lugar de /. Por ejemplo: c:\\Datos Trafico Madrid\\02-2018.csv")
print("Si introduces la ruta de otro archivo csv existente que no sea de datos de tráfico de la página del Ayuntamiento el programa no funciona :D")
print("Si introduces la ruta de un archivo que no existe te la volverá a pedir. Buena suerte.\n")

pide_ruta=True

while(pide_ruta):
	ruta=input("Ruta del archivo -> ")
	if os.path.isfile(ruta):
		pide_ruta=False
	
	if (ruta[-4:]!=".csv"):
		print("Este archivo no es un csv :(")
		pide_ruta=True

anio=int(ruta[-8:-4])  #02-2018.csv
mes=int(ruta[-11:-9])

print("Año:", anio)
print("Mes: ", mes)

if(anio<2013 or anio>2018):
	print("Año fuera de rango :(")
	pide_ruta=True

if(mes<1 or mes>12):
	print("Ese mes no existe :(")
	pide_ruta=True

datos=open(ruta, "r") 

print("Ruta introducida: ", ruta)

"""
Prueba de apertura del archivo.
cont=0

for linea in datos:
	print(linea) #imprimimos esto para saber si llega al archivo.
	cont+=1

	if cont>5: #Esto se usa para ir haciendo pruebas con las x primeras lineas del archivo
		break
"""

#Aquí se supone que ya tenemos la ruta del archivo y el archivo abierto. Procedemos a generar los archivos de datos diarios.
#Como es un proceso que tarda bastante avisamos.

print("Este proceso tarda un ratito. Puedes abrir la carpeta y ver cómo se generan los archivos. Es muy bonito.\n")

input("Pulsa enter para continuar.")

contador=0 #este contador nos va a valer para saber en que linea del archivo estamos en cada momento.

for i in datos:
	if contador==0: #nos saltamos la primera linea del archivo, la de las definiciones
		contador+=1
		#print("Estamos trabajando en ello.")
		next
		
	#elif contador==100000: #Esto se usa para ir haciendo pruebas con las x primeras lineas del archivo
	#	break

	else: 
		contador+=1
		lista=i.split(";") #Transformamos cada linea del archivo en lista
		print("La lista que generamos con la linea del archivo es: ", lista)
						
		lista_fecha=separa_fechas(lista) #generamos una nueva lista con la fecha separada :)
		
		ruta_main=os.path.dirname(os.path.abspath(__file__))

		ruta_carpeta=genera_ruta_carpeta(lista_fecha[1],lista_fecha[2],ruta_main) #nos devolverá "Directorio del main"\\Datos trafico\\mes_en_letra añoYYYY
		if not os.path.exists(ruta_carpeta): #Comprueba la existencia de la carpeta y si no existe la crea.
			os.makedirs(ruta_carpeta)

		#ahora que tenemos en lista_fecha la fecha separada deberiamos generar la ruta del archivo [1]anio [2]mes [3]dia
		ruta_archivo=genera_ruta_archivo(lista_fecha[1], lista_fecha[2], lista_fecha[3], ruta_main) #"Directorio del main"\Datos trafico\Mes_en_letra YYYY\YYYY-MM-DD
		
		#Ahora que tenemos la ruta del archivo comprobamos si existe o no el fichero diario con la funcion path.exists(file) que devuelve True si file existe
		if os.path.exists(ruta_archivo):
			resumen_diario=open(ruta_archivo, "a")
			resumen_diario.write("\n")
			resumen_diario.write(str(lista_fecha))
			resumen_diario.close()

		else:
			resumen_diario=open(ruta_archivo, "w")
			resumen_diario.write(str(lista_fecha))
			resumen_diario.close()


datos.close()
