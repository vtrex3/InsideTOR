# -*- coding: cp1252 -*-
#Autor: Armando Elorriaga
#Email: armando.elorriaga@gmail.com
from modelosBD import *
from datetime import datetime
from datetime import date
from collections import OrderedDict
import os
import time as time
import funcionesUtil



os.system("clear")
#print("Fecha ultima ejecucion: ", datetime.now())

archivo = open('/var/lib/tor/cached-microdesc-consensus')
w = 0
diccionario = {}

#Vamos leyendo el achivo y generando el diccionario.
for linea in archivo:
    linea = linea.rstrip()#Elimina salto de linea final
    
    if linea.startswith("r "):
        lineaR = linea.split(' ')
        dirIP = lineaR[5]
        
    if linea.startswith("w "):
        w = w + 1 #Cuenta los nodos existentes
        lineaW = linea.replace('w Bandwidth=','')
        velocidad = lineaW.split(' ') # a veces tiene dos terminos
        diccionario[dirIP] = int(velocidad[0])
 
archivo.close() ## Cerramos el archivo de lectura. ya lo hemos leido.

NodosPorVelocidad = OrderedDict(sorted(diccionario.items(), key=lambda x:x[1], reverse = True))
n = 0


for ip in enumerate(NodosPorVelocidad):
    if n == 100:
        break
    print("{:20}".format(ip[1]),': ',diccionario[ip[1]])
    
    #Grabamos el registro de la lectura
    regLectura = RegistroLectura()
    regLectura.fecha = datetime.now()
    regLectura.ip = ip[1]
    regLectura.anchob = diccionario[ip[1]]
    funcionesUtil.createRegistroLectura(regLectura)
    
    #Generamos estadisticas de la lectura
    #Primero vemos si el nodo ya ha sido dectado en otra lectura anterior (EL--> EstadisticasLecturas)
    EL_Old = funcionesUtil.get_EstadisticasLecturasByIP(regLectura.ip )
    #print("EL_Old: ", EL_Old)
    EL_New = EstadisticasLecturas()
    EL_New.fecha = regLectura.fecha
    EL_New.ip = regLectura.ip
    EL_New.anchob_total = regLectura.anchob
    
    if (EL_Old != None):
        #Si el nodo ya ha sido detectado anteriormente actualizamos info estadisticas con el resultado
        EL_New = funcionesUtil.prepararRegistroEL(EL_New, EL_Old)
        funcionesUtil.updateEstadisticasLecturas(EL_New)
    else:
        #Grabamos estadistica con el resultado
        EL_New = funcionesUtil.prepararRegistroEL(EL_New, None)
        funcionesUtil.createEstadisticasLecturas(EL_New)
        
   
    n = n + 1
    
     
print("Nodos existentes: ", w)    

#Grabamos el numero de nodos
regNodo = RegistroNodos()
regNodo.fecha = datetime.now()
regNodo.num_nodos = w
funcionesUtil.createRegistroNodos(regNodo)

##Generamos estadisticas de numero de nodos
#Preparamos el registro nuevo
EN_New = EstadisticasNodos()
EN_New.fecha = regNodo.fecha
EN_New.nodos_total = regNodo.num_nodos
#Obtenemos el ultimo registro de la bd.
EN_Old = funcionesUtil.get_UltimoEstadisticasNodos()

dt = None
if (EN_Old != None):
    dt = datetime.strptime(str(EN_Old.fecha), "%Y-%m-%d")

if (dt != None and dt.date() == date.today()):
    print 'Entra aqui'
    #Si ya hay un registro para ese dia lo actualizamos con los datos nuevos.
    EN_New = funcionesUtil.prepararRegistroEN(EN_New, EN_Old)
    funcionesUtil.updateEstadisticasNodos(EN_New)
else:
    #Creamos un registro nuevo de estadistica
    EN_New = funcionesUtil.prepararRegistroEN(EN_New, None)
    funcionesUtil.createEstadisticasNodos(EN_New)
 

#Originalmente se hizo con sleep pero luego se metio por cron dados los problemas que se ocasionaban
#(No actualizacion del archivo cached-microdesc-consensus)    
#time.sleep(10)
#time.sleep(3600)
#time.sleep(10800)




