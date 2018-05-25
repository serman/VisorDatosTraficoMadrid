Visor de datos de tráfico de la ciudad de Madrid.

versión 0.01-25.05.18


Notas de la versión:


Este programa permite realizar consultas sobre los datos de tráfico que publica el Ayuntamiento de Madrid en su portal de datos abiertos.

El programa se divide en dos partes fundamentales.

1.- Una funcionalidad que permite procesar los datos, separándolos por días, para facilitar su posterior uso.
2.- Un programa principal o Main que nos da una serie de opciones de consulta:

2.1.- Acceder a los valores horarios de un punto de medición dado en un periodo de tiempo dado.

  Periodo de tiempo: desde yyyy-mm-dd-hh hasta yyyy-mm-dd-hh
  Retornará los valores medios de cada una de las horas del día (la media de los cuatro valores horarios) en el medidor dado.
  
  Sirve básicamente para poder acceder a los datos de una forma ordenada.

  En este apartado nos permitirá guardar la consulta como un archivo hoja de cálculo.
  

2.2.- Acceder a la media de los valores horarios de un punto de medición dado en un periodo de tiempo dado.

  Periodo de tiempo: desde yyyy-mm-dd-hh hasta yyyy-mm-dd-hh
  Retornará un valor medio de todas las mediciones horarias comprendidas en el rango de tiempo dado.
  
  Sirve para medir la imd media en periodos de tiempo determinados (un día concreto, una hora concreta, horas punta…)
  

2.3.- Comparador de valores horarios entre dos puntos de medición dados en un periodo de tiempo dado.

  Periodo de tiempo: desde yyyy-mm-dd-hh hasta yyyy-mm-dd-hh.
  Retornará los valores medios de cada una de las horas del día en ambos medidores con la variación en %.


2.4.- Comparador de la media de los valores horarios de dos puntos de medición dados en un periodo de tiempo dado.

  Periodo de tiempo: desde yyyy-mm-dd-hh hasta yyyy-mm-dd-hh.
  Retornará la media de ambos puntos en el periodo de tiempo dado acompañado de su variación en %.




Instrucciones de uso:


1.- Descomprimir Visor_Trafico_Compartir en tu disco duro:

Hay que tener en cuenta que los datos de tráfico ocupan bastante espacio, 
que sea en una partición en la que tengas hueco suficiente (800 MB cada mes aprox).


En la carpeta descomprimida encontraremos:


- La carpeta Datos tráfico: en esta carpeta se almacenarán los datos una vez procesemos los archivos descargados de la página del ayuntamiento.

- La carpeta Módulos: aqui hay un archivo.py que contiene diferentes métodos (trozos de programa) que se utilizan en el programa principal.

- El archivo 0.- Main.py, que viene siendo el programa principal.

- El archivo 1.- Formateo de datos.py, que es una utilidad para procesar los datos y que el programa los pueda utilizar.
- El leeme.txt, que viene siendo este archivo.



2.- Tener instalado python, a partir de la versión 3.6. 

Es muy fácil de instalar y se puede encontrar aquí: https://www.python.org/downloads/



3.- Formatear los datos mensuales:

Los datos de las mediciones los cuelga el Ayuntamiento en el portal de datos abiertos en este enlace: 
https://datos.madrid.es/sites/v/index.jsp?vgnextoid=33cb30c367e78410VgnVCM1000000b205a0aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD

Aqui podemos encontrar los archivos correspondientes a los sucesivos meses (los nuevos se van añadiendo con un par de meses de margen). 
Estos archivos están en formato .csv y contienen todas las mediciones de todos los medidores cada 15 minutos, generando un archivo de muchismas líneas.

Para hacer estos datos más accesibles, junto con el programa principal viene la utilidad 1.- Formateo de datos.py. 
Este programa separa el archivo .csv archivos más pequeños correspondientes a los días de cada mes.

El proceso de transformar los datos tarda bastante pero luego hace mucho más fáciles y ágiles las búsquedas.

El tema es que para acceder a los datos de un mes en concreto, o de periodos que incluyan varios meses, hay que tener los datos descargados y procesados, 
si no el programa dará error.

Para usar la utilidad basta con darle doble click y seguir las instrucciones de pantalla, te pedirá la ruta del archivo csv 
y guardará el solito los datos dentro de la carpeta Datos tráfico, con el mes correspondiente. 

Si se le cambia el nombre a cualquiera de las carpetas o archivos el programa deja de funcionar, así que hazlo, pero solo por diversión.




4.- Hacer las consultas de datos.

Una vez formateados los datos ya se puede usar el programa 0.- Main.py 
(únicamente para fechas en las que ya tengamos los datos procesados, eso si).

El programa se ejecuta con doble click y tiene sus propias instrucciones.

El entorno es muy hostil y bastante feo porque se ejecuta en una ventana tipo MS-DOS que no deja hacer más grande, y es una de las cosas que habrá que solucionar.

Otra de las primeras mejoras será permitir que la salida sea en un documento de texto o en un documento de excel directamente.



Y ya, a pasarlo bien.