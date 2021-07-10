# -*- coding: utf-8 -*-
#Autor: Armando Elorriaga
#Email: armando.elorriaga@gmail.com

#######################
# Clases / Entidades  #
#######################

#Registro de los 100 primeros nodos que leemos cada vez
class RegistroLectura():
    id = 0
    fecha = ''
    ip = ''
    anchob = ''
    
    
#Registro de numero de nodos que leemos cada vez
class RegistroNodos():
    id = 0
    fecha = ''
    num_nodos = 0 #numero de nodos que leemos cada vez
   

#Estadisticas que sacaremos de RegistroNodos   
class EstadisticasNodos():
    id = 0
    fecha = '' #dd-mm-yyyy no horas
    nodos_total = 0 #Total de nodos en un dia
    nodos_lecturas = 0 #Veces que he leido los nodos, en teoria 8 al dia
    nodos_media = 0.0 #Media de nodos al dia
    #idem para la noche (de 20pm a 8am)
    nodos_nocturnos_total = 0 
    nodos_nocturnos_lecturas = 0
    nodos_nocturnos_media = 0.0
    #idem para el dia (de 8am a 20pm)
    nodos_diurnos_total = 0
    nodos_diurnos_lecturas = 0
    nodos_diurnos_media = 0.0
 
class EstadisticasLecturas():
    id = 0
    fecha = '' #TODOS los dias y horas a en los que se detecta el mismo nodo
    ip = ''
    num_lecturas = 0 #numero de veces detectado en el mismo dia
    anchob_total = 0 #Ancho de banda total en el dia
    anchob_media = 0.0 #Ancho de banda medio en el dia
    nocturno = 0 #numero de vece detectado en la noche
    nocturno_anchob_total = 0 #Ancho de banda total de 20pm a 8am
    nocturno_anchob_media = 0.0 #Ancho de banda medio de 20pm a 8am
    diurno = 0 # numero de veces detectado en el dia
    diurno_anchob_total = 0 #Ancho de banda total de 8am a 20pm
    diurno_anchob_media = 0.0 #Ancho de banda medio de 8am a 20pm
    
    