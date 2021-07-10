# -*- coding: utf-8 -*-
#Autor: Armando Elorriaga
#Email: armando.elorriaga@gmail.com
import psycopg2
from datetime import datetime, timedelta
from modelosBD import *
import json, datetime

#Constantes
BASE_DATOS = 'estadisticas' 
IP_BD = '192.168.1.16'
USUARIO = 'mandi'
PASSWORD = 'mandi'
PUERTO = '5432'


#############################
# FUNCIONES UTIL            #
# MANEJO DE LA BD           #
#############################

# Conexion de la bd 
def conectar():
    #String de conexion
    conn_string = "host=" + IP_BD + " port=" + PUERTO + " dbname=" + BASE_DATOS + " user=" + USUARIO + " password=" + PASSWORD
    
    try:
        conn = psycopg2.connect(conn_string)
    except:
        logger.error("Error en conexion BD: %s", conn_string)
    
    return conn
    
    
# Dexconexion de la bd 
def desconectar(conexion):
    if conexion is not None:
        conexion.close()
        
        

# Creacion de registro de datos de lo nodos por lectura
def createRegistroLectura(RegistroLectura):
    consulta = "insert into registros_lecturas (fecha, ip, anchob) " \
        "values ('%s', '%s', %s);" %(RegistroLectura.fecha, RegistroLectura.ip , RegistroLectura.anchob)
    #print("consulta: ", consulta)
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute(consulta)
        conexion.commit()
        cursor.close()
        desconectar(conexion)
        return 0
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error en consulta createRegistroLectura: ", error)
        desconectar(conexion)
        return 1
        
        
# Creacion de registro del numero de nodos por lectura
def createRegistroNodos(RegistroNodos):
    consulta = "insert into registro_nodos (fecha, num_nodos) " \
        "values ('%s', %s);" %(RegistroNodos.fecha, RegistroNodos.num_nodos)
    #print("consulta: ", consulta)
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute(consulta)
        conexion.commit()
        cursor.close()
        desconectar(conexion)
        return 0
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error en CREATE RegistroNodos: ", error)
        desconectar(conexion)
        return 1
        

# Creacion de registro de EstadisticasLecturas por dia
def createEstadisticasLecturas(EstadisticasLecturas):
    consulta = "insert into estadisticas_lecturas (fecha, ip, num_lecturas, anchob_total, anchob_media, "\
        "nocturno, nocturno_anchob_total, nocturno_anchob_media, diurno, diurno_anchob_total, diurno_anchob_media) " \
        "values ('%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s);" %(EstadisticasLecturas.fecha, EstadisticasLecturas.ip, EstadisticasLecturas.num_lecturas,
        EstadisticasLecturas.anchob_total, EstadisticasLecturas.anchob_media, EstadisticasLecturas.nocturno, EstadisticasLecturas.nocturno_anchob_total,
        EstadisticasLecturas.nocturno_anchob_media, EstadisticasLecturas.diurno, EstadisticasLecturas.diurno_anchob_total , EstadisticasLecturas.diurno_anchob_media)
    #print("consulta: ", consulta)   
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute(consulta)
        conexion.commit()
        cursor.close()
        desconectar(conexion)
        return 0
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error en consulta createEstadisticasLecturas: ", error)
        desconectar(conexion)
        return 1
        
        
# Creacion de registro de EstadisticasNodos por dia
def createEstadisticasNodos(EstadisticasNodos):
    consulta = "insert into estadisticas_nodos (fecha, nodos_total, nodos_lecturas, nodos_media, nodos_nocturnos_total, "\
        "nodos_nocturnos_lecturas, nodos_nocturnos_media, nodos_diurnos_total, nodos_diurnos_lecturas, nodos_diurnos_media) " \
        "values ('%s', %s, %s, %s, %s, %s, %s, %s, %s, %s);" %(EstadisticasNodos.fecha, EstadisticasNodos.nodos_total, EstadisticasNodos.nodos_lecturas,
        EstadisticasNodos.nodos_media, EstadisticasNodos.nodos_nocturnos_total, EstadisticasNodos.nodos_nocturnos_lecturas, EstadisticasNodos.nodos_nocturnos_media,
        EstadisticasNodos.nodos_diurnos_total, EstadisticasNodos.nodos_diurnos_lecturas, EstadisticasNodos.nodos_diurnos_media)
    #print("consulta: ", consulta)   
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute(consulta)
        conexion.commit()
        cursor.close()
        desconectar(conexion)
        return 0
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error en consulta createEstadisticasNodos: ", error)
        desconectar(conexion)
        return 1

        
#Busqueda de ip (nodo) en estadisticas_lecturas
def get_EstadisticasLecturasByIP(ip_nodo):
    records = None
    consulta = "select * from estadisticas_lecturas where ip='%s';" %ip_nodo
    #print("consulta: ", consulta)
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute(consulta)
        records = [dict((cursor.description[i][0], value) \
            for i, value in enumerate(row)) for row in cursor.fetchall()]
        cursor.close()
        desconectar(conexion)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error en consulta get_EstadisticasLecturasByIP: ", error)
        desconectar(conexion)
        
    if records:
        return serializaEL(records[0])
    return None
 
 
#ASctualizacion de registro de EstadisticasLecturas en el mismo dia
def updateEstadisticasLecturas(EstadisticasLecturas):
    consulta = "update estadisticas_lecturas set fecha='%s', num_lecturas=%s, anchob_total=%s, anchob_media=%s, "\
        "nocturno=%s, nocturno_anchob_total=%s, nocturno_anchob_media=%s, diurno=%s, diurno_anchob_total=%s, "\
        " diurno_anchob_media=%s where id=%s;" \
        %(EstadisticasLecturas.fecha, EstadisticasLecturas.num_lecturas,EstadisticasLecturas.anchob_total, EstadisticasLecturas.anchob_media,
         EstadisticasLecturas.nocturno, EstadisticasLecturas.nocturno_anchob_total, EstadisticasLecturas.nocturno_anchob_media,
         EstadisticasLecturas.diurno, EstadisticasLecturas.diurno_anchob_total, EstadisticasLecturas.diurno_anchob_media, EstadisticasLecturas.id)
    #print("consulta: ", consulta)    
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute(consulta)
        conexion.commit()
        cursor.close()
        desconectar(conexion)
        return 0
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error en consulta updateEstadisticasLecturas: ", error)
        desconectar(conexion)
        return 1
        
        
#Actualizacion de registro de EstadisticasNodos
def updateEstadisticasNodos(EstadisticasNodos):
    consulta = "update estadisticas_nodos set nodos_total=%s, nodos_lecturas=%s, nodos_media=%s, nodos_nocturnos_total=%s, "\
        "nodos_nocturnos_lecturas=%s, nodos_nocturnos_media=%s, nodos_diurnos_total=%s, nodos_diurnos_lecturas=%s, nodos_diurnos_media=%s where id=%s;" \
        %(EstadisticasNodos.nodos_total, EstadisticasNodos.nodos_lecturas, EstadisticasNodos.nodos_media, 
        EstadisticasNodos.nodos_nocturnos_total, EstadisticasNodos.nodos_nocturnos_lecturas, EstadisticasNodos.nodos_nocturnos_media,
        EstadisticasNodos.nodos_diurnos_total, EstadisticasNodos.nodos_diurnos_lecturas , EstadisticasNodos.nodos_diurnos_media, EstadisticasNodos.id)
    #print("consulta: ", consulta)    
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute(consulta)
        conexion.commit()
        cursor.close()
        desconectar(conexion)
        return 0
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error en consulta updateEstadisticasNodos: ", error)
        desconectar(conexion)
        return 1
 
 
 
#Obtiene el utlimo registro de EstadisticasNodos
def get_UltimoEstadisticasNodos():
    records = None
    consulta = "select * from estadisticas_nodos order by id desc limit 1;"
    #print("consulta: ", consulta)
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute(consulta)
        records = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
        cursor.close()
        desconectar(conexion)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error en consulta get_UltimoEstadisticasNodos: ", error)
        desconectar(conexion)
        
    if records:
        return serializaEN(records[0])
    return None
 
 
 
  
 
 
#############################
# FUNCIONES UTIL            #
# CALCULOS ACTUALIZACIONES  #
#############################

#Actualizacion de registro tipo EstadisticasLecturas con la informacion nueva y la que se tenia
def prepararRegistroEL(EL_New, EL_Old):
    actual = EstadisticasLecturas()
    actual.ip = EL_New.ip
    if (EL_Old != None):
        #El nodo ya lo hemos detectado otras veces.
        actual.id = EL_Old.id
        actual.fecha = EL_Old.fecha + ' y ' +  str(EL_New.fecha) #Vamos guardando todas las fechas en elas que se detecta el nodo.
        actual.num_lecturas = 1 + EL_Old.num_lecturas
        actual.anchob_total = EL_New.anchob_total + EL_Old.anchob_total
        actual.anchob_media = actual.anchob_total / actual.num_lecturas
        
        #Miramos la fecha del registro para saber cuando se ha detectado (noche o dia en España)
        if (esDiurno(EL_New.fecha)):
            actual.diurno = EL_Old.diurno + 1
            actual.diurno_anchob_total = EL_New.anchob_total + EL_Old.diurno_anchob_total
            actual.diurno_anchob_media =  actual.diurno_anchob_total / actual.diurno
            #Estadisticas nocturnas no cambian
            actual.nocturno = EL_Old.nocturno
            actual.nocturno_anchob_total = EL_Old.nocturno_anchob_total
            actual.nocturno_anchob_media = EL_Old.nocturno_anchob_media
            
        else:
            actual.nocturno = EL_Old.nocturno + 1
            actual.nocturno_anchob_total = EL_New.anchob_total + EL_Old.nocturno_anchob_total
            actual.nocturno_anchob_media =  actual.nocturno_anchob_total / actual.nocturno
            #Estadisticas diarias no cambian
            actual.diurno = EL_Old.diurno
            actual.diurno_anchob_total = EL_Old.diurno_anchob_total
            actual.diurno_anchob_media = EL_Old.diurno_anchob_media
        
    else:
        #Es la primera vez que nos encontramos este nodo
        actual.fecha = EL_New.fecha 
        actual.num_lecturas = 1
        actual.anchob_total = EL_New.anchob_total
        actual.anchob_media = EL_New.anchob_total
        #Miramos la fecha del registro para saber cuando se ha detectado (noche o dia en España)
        if (esDiurno(EL_New.fecha)):
            actual.diurno = 1
            actual.diurno_anchob_total = EL_New.anchob_total
            actual.diurno_anchob_media =  EL_New.anchob_total
            #Estadisticas nocturnas no cambian
            actual.nocturno = 0
            actual.nocturno_anchob_total = 0
            actual.nocturno_anchob_media = 0.0
            
        else:
            actual.nocturno = 1
            actual.nocturno_anchob_total = EL_New.anchob_total
            actual.nocturno_anchob_media =  EL_New.anchob_total
            #Estadisticas diarias no cambian
            actual.diurno = 0
            actual.diurno_anchob_total = 0
            actual.diurno_anchob_media = 0.0
     
    return actual  
       

       
#Comprobar si esta en horario diurno o nocturno. 
def esDiurno(fecha):
    diurno = ("08:00", "19:59")
    #noche = ("21:00", "07:59")
    fecha = datetime.datetime.strptime(str(fecha), '%Y-%m-%d %H:%M:%S.%f')
    hora = fecha.strftime('%H:%M')
    return (hora >= diurno[0] and hora <= diurno[1]) #True si es de diurno, False si es nocturno
        
  

#Actualizar las estadisticas del numero de nodos.
#TODO- Comprobar que la fecha es correcta.  
def prepararRegistroEN(EN_New, EN_Old):
    actual = EstadisticasNodos()
    #Si es el primer registro
    if (EN_Old == None):
        #fecha = datetime.strptime(EN_New.fecha, '%d-%m-%Y')
        actual.fecha = EN_New.fecha
        actual.nodos_total = EN_New.nodos_total
        actual.nodos_lecturas = 1
        actual.nodos_media = actual.nodos_total
        
        if (esDiurno(EN_New.fecha)):
            actual.nodos_diurnos_total = actual.nodos_total
            actual.nodos_diurnos_lecturas = 1
            actual.nodos_diurnos_media = actual.nodos_total
            actual.nodos_nocturnos_total = 0
            actual.nodos_nocturnos_lecturas = 0
            actual.nodos_nocturnos_media = 0.0
        else:
            actual.nodos_nocturnos_total = EN_New.nodos_nocturnos_total
            actual.nodos_nocturnos_lecturas = 1
            actual.nodos_nocturnos_media = EN_New.nodos_nocturnos_total
            actual.nodos_diurnos_total = 0
            actual.nodos_diurnos_lecturas = 0
            actual.nodos_diurnos_media = 0.0
        
    else:
        actual.id = EN_Old.id
        actual.fecha = EN_Old.fecha
        actual.nodos_total = EN_New.nodos_total + EN_Old.nodos_total
        actual.nodos_lecturas = EN_Old.nodos_lecturas + 1
        actual.nodos_media = actual.nodos_total / actual.nodos_lecturas
        
        if (esDiurno(EN_New.fecha)):
            actual.nodos_diurnos_total = EN_New.nodos_total + EN_Old.nodos_diurnos_total
            actual.nodos_diurnos_lecturas = EN_Old.nodos_diurnos_lecturas + 1
            actual.nodos_diurnos_media = actual.nodos_diurnos_total / actual.nodos_diurnos_lecturas
            #Los nocturnos no cambian
            actual.nodos_nocturnos_total = EN_Old.nodos_nocturnos_total
            actual.nodos_nocturnos_lecturas = EN_Old.nodos_nocturnos_lecturas
            actual.nodos_nocturnos_media = EN_Old.nodos_nocturnos_media
        else:
            actual.nodos_nocturnos_total = EN_New.nodos_total + EN_Old.nodos_nocturnos_total
            actual.nodos_nocturnos_lecturas = EN_Old.nodos_nocturnos_lecturas + 1
            actual.nodos_nocturnos_media = actual.nodos_nocturnos_total / actual.nodos_nocturnos_lecturas
            #Los diurnos no cambian
            actual.nodos_diurnos_total = EN_Old.nodos_diurnos_total
            actual.nodos_diurnos_lecturas = EN_Old.nodos_diurnos_lecturas
            actual.nodos_diurnos_media = EN_Old.nodos_diurnos_media
 
    return actual
 
 
#Serializar un objeto a tipo EstadisticasLecturas
def serializaEL(registro):
    regAux = EstadisticasLecturas()
    regAux.id = registro['id']
    regAux.fecha = registro['fecha']
    regAux.ip = registro['ip']
    regAux.num_lecturas = registro['num_lecturas']
    regAux.anchob_total = registro['anchob_total']
    regAux.anchob_media = registro['anchob_media']
    regAux.nocturno = registro['nocturno']
    regAux.nocturno_anchob_total = registro['nocturno_anchob_total']
    regAux.nocturno_anchob_media = registro['nocturno_anchob_media']
    regAux.diurno = registro['diurno']
    regAux.diurno_anchob_total = registro['diurno_anchob_total']
    regAux.diurno_anchob_media = registro['diurno_anchob_media']

    return regAux
    
    
    
  
#Serializar un objeto a tipo EstadisticasNodos
def serializaEN(registro):
    regAux = EstadisticasNodos()
    regAux.id = registro['id']
    regAux.fecha = registro['fecha']
    regAux.nodos_total = registro['nodos_total']
    regAux.nodos_lecturas = registro['nodos_lecturas']
    regAux.nodos_media = registro['nodos_media']
    regAux.nodos_nocturnos_total = registro['nodos_nocturnos_total']
    regAux.nodos_nocturnos_lecturas = registro['nodos_nocturnos_lecturas']
    regAux.nodos_nocturnos_media = registro['nodos_nocturnos_media']
    regAux.nodos_diurnos_total = registro['nodos_diurnos_total']
    regAux.nodos_diurnos_lecturas = registro['nodos_diurnos_lecturas']
    regAux.nodos_diurnos_media = registro['nodos_diurnos_media']

    return regAux
    
 