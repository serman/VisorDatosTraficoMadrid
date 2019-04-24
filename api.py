"""

Aqui vamos a poner el menu principal que de acceso a las diferentes funciones.

1.- Ver mapa de puntos de medida.

2.- Ver datos que ofrece cada punto de medida

3.- Acceder a los valores horarios de un punto de medición dado en un periodo de tiempo dado.

  Periodo de tiempo: desde yyyy-mm-dd-hh hasta yyyy-mm-dd-hh
  Retornará los valores medios de cada una de las horas del día (la media de los cuatro valores horarios) en el medidor dado.

  Sirve básicamente para poder acceder a los datos de una forma ordenada.


4.- Acceder a la media de los valores horarios de un punto de medición dado en un periodo de tiempo dado.

  Periodo de tiempo: desde yyyy-mm-dd-hh hasta yyyy-mm-dd-hh
  Retornará un valor medio de todas las mediciones horarias comprendidas en el rango de tiempo dado.

  Sirve para medir la imd media en periodos de tiempo determinados (un día concreto, una hora concreta, horas punta…)


5.- Comparador de valores horarios entre dos puntos de medición dados en un periodo de tiempo dado.

  Periodo de tiempo: desde yyyy-mm-dd-hh hasta yyyy-mm-dd-hh.
  Retornará los valores medios de cada una de las horas del día en ambos medidores con la variación en %.

6.- Comparador de la media de los valores horarios de dos puntos de medición dados en un periodo de tiempo dado.

  Periodo de tiempo: desde yyyy-mm-dd-hh hasta yyyy-mm-dd-hh.
  Retornará la media de ambos puntos en el periodo de tiempo dado acompañado de su variación en %.


De momento sólo podemos usar los conjuntos de datos a partir de enero de 2015, los datos anteriores tienen
un formato distinto y hay que adaptarlos para que la ID de los lectores sea unívoca.

"""

from io import open
from .Modulos.Modulos import *
import os.path
import os
import openpyxl
from openpyxl import Workbook

ruta_main=os.path.dirname(os.path.abspath(__file__))

def medidorPeriodo(id_medidor,anio_inicial, mes_inicial, dia_inicial, hora_inicial, anio_final, mes_final, dia_final, hora_final, porMinutos):
    medidor3=id_medidor #medidor de la opción 3, por si utilizamos otras variables medidor en el programa, para que esta quede limpia.
    #Llamamos a pidedias
    fechas3= [anio_inicial, mes_inicial, dia_inicial, hora_inicial, anio_final, mes_final, dia_final, hora_final]
    #Llamamos a genera_fechas, que nos pide       (anio_inicial, mes_inicial, dia_inicial, hora_inicial, anio_final, mes_final, dia_final, hora_final)  ->  Lista de listas: [año] [mes] [dia] [hora inicial] [hora final]
    lista_fechas3=genera_fechas(fechas3[0],fechas3[1],fechas3[2],fechas3[3],fechas3[4],fechas3[5],fechas3[6],fechas3[7])

    #aqui gestionamos cómo va a querer el usuario que se muestren los datos, si en mediciones horarias o cada 15 minutos

    minutos3=porMinutos

    #operador3=porMinutos #por minutos o por horas



    #Ya tenemos el código del medidor en medidor3 y la lista de fechas del periodo en lista_fechas3, ahora accedemos a los datos y los imprimimos en pantalla.
    #Para ello utilizamos la función extrae líneas y la función genera_ruta

    """
     def extrae_lineas(codigo, ruta_archivo, hora_inicial, hora_final): -> lista de listas donde cada línea es:

     [0]clave          int
     [1]fecha_anio     int
     [2fecha_mes       int
     [3]fecha_dia      int
     [4]fecha_hora     int
     [5]fecha_minuto   int
     [6]=descripcion   string
     [7]=intensidad    int
     [8]=ocupacion     int
     [9]=carga         int
     [10]=vmed         int
     [11]=error        string
     [12]=periodo      int
    """
    # def genera_ruta_archivo(anio, mes, dia, ruta_main): -> "Directorio del main"\\Datos Trafico Madrid\\Febrero 2018\\2018-02-03
    lista_final=[]
    for i in lista_fechas3:
      rutai=genera_ruta_archivo(i[0], i[1], i[2], ruta_main) #genera_ruta_archivo(año, mes, dia, ruta_main)
      listai=extrae_lineas(medidor3, rutai, i[3], i[4])
      outputStr=""
      print (lista_fechas3)
      #print ("lista i")
      #print(listai)
      #print(rutai)

      if(minutos3):
          lista_final=lista_final+listai
        #for j in listai:
        #  outputStr += (f"El medidor {medidor3} el día {j[3]} del mes {j[2]} del año {j[1]} a las {j[4]} horas y {j[5]} minutos tuvo unas mediciones de {j[7]} intensidad, {j[8]} ocupación, {j[9]} carga y {j[10]} velocidad media")

      else: #Aquí habría que hacer una nueva llamada a la función agrupar_mediciones_horarias(lista_origen): -> lista de listas con los valores horarios
        lista_horariai=agrupar_mediciones_horarias(listai)
        lista_final=lista_final+lista_horariai
        #for j in lista_horariai:
        #  outputStr += (f"El medidor {medidor3} el día {j[3]} del mes {j[2]} del año {j[1]} a las {j[4]} horas tuvo unas mediciones de {j[7]} intensidad, {j[8]} ocupación, {j[9]} carga y {j[10]} velocidad media con {j[13]} mediciones en esa hora.")


    return lista_final, medidor3
