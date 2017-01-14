#coding=utf-8
from django.shortcuts import render
from django.db import connection

import PyICU


from .models import Alumno, Calificacion, Modulo
# Create your views here.


def index(peticion):
    contexto={
        "titulo":"Titulo"
    }
    return render(peticion, "bd/base.html", contexto)


def ordenar_lista_modelos(lista_modelos):
    locale=PyICU.Locale("es_ES")
    collator = PyICU.Collator.createInstance(locale)
    apellidos=[]
    for m in lista_modelos:
        apellidos.append(m.apellidos)
    apellidos=sorted(apellidos, key=collator.getSortKey)
    nueva_lista=[]
    for a in apellidos:
        nueva_lista.append(Alumno.objects.filter(apellidos=a)[0])
    return nueva_lista
    
    


def cuantos_alumnos_con_x_suspensas(filas, x):
    """Dadas las filas con estadisticas nos dice cuantos alumnos han suspendido
    2, 3 o x materias. Si no encuentra ninguna devuelve 0"""
    
    for fila in filas:
        if fila[0]==x:
            return fila[1]
    return 0

def cuantos_alumnos_con_x_o_mas_suspensas(filas,  x, cantidad_modulos):
    total=0
    for cantidad_suspensas in range(x, cantidad_modulos+1):
        total=total+cuantos_alumnos_con_x_suspensas(filas, cantidad_suspensas)
    return total
        
    
def estadisticas_con_x_o_mas_suspensas(filas, x, cantidad_modulos):
    estadisticas=[]
    for cantidad_suspensas in range(0, x):
        texto="Alumnos con {0} suspensas".format(cantidad_suspensas)
        cantidad_suspensas=cuantos_alumnos_con_x_suspensas(filas, cantidad_suspensas)
        estadisticas.append ( (texto, cantidad_suspensas))
    texto="Alumnos con {0} o más suspensas".format(x)
    cantidad_suspensas=cuantos_alumnos_con_x_o_mas_suspensas(filas, x, cantidad_modulos)
    estadisticas.append ( (texto, cantidad_suspensas))
    return estadisticas

        
def estadisticas_totales(filas, cantidad_modulos):
    estadisticas=[]
    for cantidad_suspensas in range(0, cantidad_modulos+1):
        texto="Alumnos con {0} suspensas".format(cantidad_suspensas)
        cantidad_suspensas=cuantos_alumnos_con_x_suspensas(filas, cantidad_suspensas)
        estadisticas.append ( (texto, cantidad_suspensas))
    return estadisticas

def estadisticas_evaluacion(peticion, evaluacion):
    consulta="""
        select suspensas, count(suspensas) from (select alumno_id,count(*)  as suspensas
            from bd_calificacion
                where conv=0 and apro=0 and calificacion<5 and ev=%s
                group by alumno_id
            )
        group by suspensas
    """
    CANTIDAD_MODULOS_DAM=7
    
    with connection.cursor() as cursor:
        cursor.execute(consulta,[evaluacion])
        filas=cursor.fetchall()
    
    #Calculamos las distintas estadisticas para las filas de resultados
    estadisticas_completas=estadisticas_totales(filas, CANTIDAD_MODULOS_DAM)
    estadisticas_con_4_o_mas_suspensas=estadisticas_con_x_o_mas_suspensas(filas, 4, CANTIDAD_MODULOS_DAM)
    estadisticas_con_3_o_mas_suspensas=estadisticas_con_x_o_mas_suspensas(filas, 3, CANTIDAD_MODULOS_DAM)
    contexto={
        "titulo":"Estadisticas evaluacion {0}".format(evaluacion),
        "num_eval":evaluacion,
        "estadisticas_totales":estadisticas_completas,
        "estadisticas_con_4_o_mas":estadisticas_con_4_o_mas_suspensas,
        "estadisticas_con_3_o_mas":estadisticas_con_3_o_mas_suspensas
    }
    return render(peticion, "bd/estadisticas.html", contexto)

def acta_evaluacion(peticion, evaluacion):
    
    alumnos=Alumno.objects.all()
    print(alumnos)
    alumnos=ordenar_lista_modelos(alumnos)
    print(alumnos)
    calificaciones=Calificacion.objects.filter(ev=evaluacion)
    filas=[]
    modulos=Modulo.objects.all()
    nombres_modulo=[]
    encabezamientos=[]
    for m in modulos:
        nombres_modulo.append(m.nombre)
    encabezamientos=["Apellidos", "Nombre"]+nombres_modulo
    
    for a in alumnos:
        print(a)
        notas=[]
        for m in modulos:
            calificaciones=Calificacion.objects.filter(ev=evaluacion, alumno=a, modulo=m)
            
            for c in calificaciones:
                if c.apro:
                    notas.append("APRO")
                    continue
                if c.conv:
                    notas.append("CONV")
                    continue
                notas.append(c.calificacion)
                
        filas.append( [a.apellidos, a.nombre]+notas)
    
    contexto={
        "titulo":"Acta de evaluacion",
        "num_eval":evaluacion,
        "encabezamientos":encabezamientos,
        "filas":filas
    }
    
    return render(peticion, "bd/acta.html", contexto)