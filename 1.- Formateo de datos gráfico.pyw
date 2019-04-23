from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from contextlib import ExitStack
import math
from io import open
import os.path
import os
from pathlib import Path
from Modulos.Modulos import *
import shutil

#----------------------------------------------------------

root=Tk()

root.title("Utilidad de formateo de datos")

#root.iconbitmap("marvin.ico") #Poner el icono

#VARIABLES

ficheroSeleccionado=False
fichero="No hay fichero seleccionado"


#FUNCIONES

def cargarArchivo():

	global fichero
	global ficheroSeleccionado

	fichero= filedialog.askopenfilename(title = "Selecciona archivo CSV", filetypes = (("CSV Files","*.csv"),))
	contenidoEtiquetaArchivo.set(fichero) #modificamos para que muestre el contenido de la variable fichero en la etiqueta correspondiente
	ficheroSeleccionado=True #para saber que ya tenemos un fichero cargado
	print(ficheroSeleccionado)
	#print(fichero)


def salirAplicacion():
	valor=messagebox.askquestion("Salir","Deseas salir de la aplicación")

	if valor=="yes":
		root.destroy()


def procesarFichero():

	#print(procesarFichero)
	
	#if (ficheroSeleccionado==True):

	#Creamos la ruta de la carpeta en la que vamos a almacenar los resultados.

	global fichero

	ruta_main=os.path.dirname(os.path.abspath(__file__))

	print(fichero)

	anio=int(fichero[-8:-4])  #02-2018.csv
	mes=int(fichero[-11:-9])

	print("Año:", anio)
	print("Mes: ", mes)

	ruta_carpeta=genera_ruta_carpeta(anio,mes,ruta_main) #nos devolverá "Directorio del main"\\Datos trafico\\mes_en_letra añoYYYY

	if not os.path.exists(ruta_carpeta): #Comprueba la existencia de la carpeta y si no existe la crea.
		os.makedirs(ruta_carpeta)


	#Generamos una carpeta auxiliar temp dentro de la carpeta de resultados
	#OJO!!!, cambiar esto, para la prueba lo hacemos en la ruta archivo

	ruta_carpeta_temp=fichero[:-11] + "temp\\" #le quitamos el nombre del archivo, los últimos 11 caracteres

	#print("Ruta archivo: ", ruta_archivo)
	#print("Ruta carpeta temporal: ", ruta_carpeta_temp)

	try:
		os.makedirs(ruta_carpeta_temp)
	except FileExistsError:
		next

	#Ahora habría que llamar a la función splitcsv, convenientemente alojada en la librería que corresponda
	#Vamos a probar a dividir el archivo en 8 partes

	split_csv(fichero, ruta_carpeta_temp, 8)


	#Almacenamos la ruta de los archivos en una lista

	lista_archivos_temp=ls(ruta_carpeta_temp)


	#Procesamos cada uno de los archivos por separado, ojo que no pise el contenido de los anteriores

	for i in lista_archivos_temp:
		ruta_i=ruta_carpeta_temp+i #añadimos al nombre de archivo la ruta de la carpeta en la que se encuentra.
		#print("Vamos a procesar el trozo: ", ruta_i)
		datos_i=open(ruta_i, "r")

		for j in datos_i:
			lista=j.split(";") #Transformamos cada linea del archivo en lista
			#print("La lista que generamos con la linea del archivo es: ", lista)
							
			lista_fecha=separa_fechas(lista) #generamos una nueva lista con la fecha separada :)
			
			ruta_main=os.path.dirname(os.path.abspath(__file__))

			ruta_carpeta=genera_ruta_carpeta(lista_fecha[1],lista_fecha[2],ruta_main) #nos devolverá "Directorio del main"\\Datos trafico\\mes_en_letra añoYYYY
			if not os.path.exists(ruta_carpeta): #Comprueba la existencia de la carpeta y si no existe la crea.
				os.makedirs(ruta_carpeta)

			#ahora que tenemos en lista_fecha la fecha separada deberiamos generar la ruta del archivo [1]anio [2]mes [3]dia
			ruta_archivo=genera_ruta_archivo(lista_fecha[1], lista_fecha[2], lista_fecha[3], ruta_main) #"Directorio del main"\Datos trafico\Mes_en_letra YYYY\YYYY-MM-DD
			
			#Ahora que tenemos la ruta del archivo añadimos la línea correspondiente. Hacemos el if-elif para que no quede una línea en blanco al principio del archivo
			
			#si el archivo no existe:
			if not os.path.exists(ruta_archivo):
				resumen_diario=open(ruta_archivo, "a") #abro el archivo en formato append, como no está, lo crea
				resumen_diario.write(str(lista_fecha)) #añado la línea 
				resumen_diario.close() #cierro el archivo

			elif os.path.exists(ruta_archivo):
				resumen_diario=open(ruta_archivo, "a") #abro el archivo en formato append
				resumen_diario.write("\n") #metemos un salto de línea para que la nueva línea se añada a continuación de la anterior
				resumen_diario.write(str(lista_fecha)) #añadimos la línea
				resumen_diario.close() #ciero el archivo
			
		

		datos_i.close() 

	#Borramos los archivos troceados y la carpeta auxiliar

	shutil.rmtree(ruta_carpeta_temp)


	#else:

	#	messagebox.showinfo("Error", "No hay fichero seleccionado")

#MENU

barraMenu=Menu(root)
root.config(menu=barraMenu, width=300, height=300)

#Construir elementos

menuArchivo=Menu(barraMenu, tearoff=0)
menuArchivo.add_command(label="Seleccionar archivo", command=cargarArchivo)
menuArchivo.add_separator()
menuArchivo.add_command(label="Salir", command=salirAplicacion)

menuAyuda=Menu(barraMenu, tearoff=0)
menuAyuda.add_command(label="Instrucciones")
menuAyuda.add_command(label="Acerca de...")

#Añadir elementos a la barra

barraMenu.add_cascade(label="Archivo", menu=menuArchivo)
barraMenu.add_cascade(label="Ayuda", menu=menuAyuda)


#Texto explicativo

frameTexto=Frame(root, width=1000, height=200)
frameTexto.pack()

texto=Label(frameTexto, text="Para poder acceder a los datos de los diferentes medidores primero hay que procesar el archivo con los datos mensuales. \nEste archivo es el que podemos descargar del portal de Datos Abiertos. \nPara poder acceder al archivo te vamos a pedir la ruta de archivo, los datos resultantes se guardarán dentro de la carpeta en la que está el ejecutable, en Datos trafico.", fg="Green")
texto.place(x=1, y=1) #ubica el texto dentro del frame en las coordenadas que le pasemos


#BOTONES DE SELECCIONAR ARCHIVO Y DE PROCESAR ARCHIVO Y ETIQUETAS

frameBotones=Frame(root, width=600, height=100)
frameBotones.pack()

#Constuimos las etiquetas

contenidoEtiquetaArchivo=StringVar() #Definimos un stringvar que será el contenido de la etiqueta archivo
contenidoEtiquetaArchivo.set(fichero) #La modificamos para que contenga el contenido de la variable fichero, que almacenará la ruta del archivo

etiquetaArchivo=Label(frameBotones, textvariable=contenidoEtiquetaArchivo)
etiquetaArchivo.grid(row=0, column=1, padx=10, pady=10)


#Construimos los botones

botonCargarFichero=Button(frameBotones, text="Seleccionar archivo", command=cargarArchivo)
botonCargarFichero.grid(row=0, column=0, sticky="e", padx=1, pady=1)

botonProcesarFichero=Button(frameBotones, text="Procesar archivo", command=procesarFichero)
botonProcesarFichero.grid(row=1, column=0, padx=1, pady=1)


###################### aquí en algún momento molaría poner unas cajitas para que muestre el año y mes del archivo seleccionado, y ya luego comprobar también si están dentro de los rangos válidos
"""
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
"""


root.mainloop()