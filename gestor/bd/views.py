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
        
    
def get_porcentaje (num1, num2):
    porcentaje=num1*100/num2
    return "{0:4.3}".format(porcentaje)


def estadisticas_con_x_o_mas_suspensas(filas, x, cantidad_modulos, total_alumnos):
    estadisticas=[]
    for cantidad_suspensas in range(1, x):
        texto="Alumnos con {0} suspensas".format(cantidad_suspensas)
        cantidad_suspensas=cuantos_alumnos_con_x_suspensas(filas, cantidad_suspensas)
        porcentaje=get_porcentaje(cantidad_suspensas, total_alumnos)
        #porcentaje=cantidad_suspensas*100/total_alumnos
        estadisticas.append ( (texto, cantidad_suspensas, porcentaje))
    texto="Alumnos con {0} o más suspensas".format(x)
    cantidad_suspensas=cuantos_alumnos_con_x_o_mas_suspensas(filas, x, cantidad_modulos)
    #porcentaje=cantidad_suspensas*100/total_alumnos
    porcentaje=get_porcentaje(cantidad_suspensas, total_alumnos)
    estadisticas.append ( (texto, cantidad_suspensas, porcentaje))
    return estadisticas

        
def estadisticas_totales(filas, cantidad_modulos, total_alumnos):
    estadisticas=[]
    for cantidad_suspensas in range(1, cantidad_modulos+1):
        texto="Alumnos con {0} suspensas".format(cantidad_suspensas)
        cantidad_suspensas=cuantos_alumnos_con_x_suspensas(filas, cantidad_suspensas)
        porcentaje=get_porcentaje(cantidad_suspensas, total_alumnos)
        #porcentaje=cantidad_suspensas*100/total_alumnos
        estadisticas.append ( (texto, cantidad_suspensas, porcentaje))
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
    
    consulta_todos_modulos_aprobados="""
       select count (distinct alumno_id) from bd_calificacion where alumno_id not in (select alumno_id from bd_calificacion as c2 where 
                c2.calificacion<5 and conv=0 and apro=0 and ev=%s)
    """
    CANTIDAD_MODULOS_DAM=7
    
    with connection.cursor() as cursor:
        cursor.execute(consulta,[evaluacion])
        filas=cursor.fetchall()
        cursor.execute(consulta_todos_modulos_aprobados,[evaluacion])
        fila_alumnos_todos_modulos_aprobados=cursor.fetchall()
    
    alumnos=Alumno.objects.all()
    total_alumnos=len(alumnos)
    
    cantidad_alumnos_todos_modulos_aprobados=int(fila_alumnos_todos_modulos_aprobados[0][0])
    porcentaje=cantidad_alumnos_todos_modulos_aprobados*100/total_alumnos
    print (total_alumnos, cantidad_alumnos_todos_modulos_aprobados, porcentaje)
    tupla_todo_aprobado=[("Alumnos con 0 suspensas", cantidad_alumnos_todos_modulos_aprobados, porcentaje)]
    
    
    #Calculamos las distintas estadisticas para las filas de resultados
    estadisticas_completas=estadisticas_totales(filas, CANTIDAD_MODULOS_DAM, total_alumnos)
    estadisticas_completas=tupla_todo_aprobado + estadisticas_completas
    estadisticas_con_4_o_mas_suspensas=estadisticas_con_x_o_mas_suspensas(filas, 4, CANTIDAD_MODULOS_DAM, total_alumnos)
    estadisticas_con_4_o_mas_suspensas=tupla_todo_aprobado + estadisticas_con_4_o_mas_suspensas
    estadisticas_con_3_o_mas_suspensas=estadisticas_con_x_o_mas_suspensas(filas, 3, CANTIDAD_MODULOS_DAM, total_alumnos)
    estadisticas_con_3_o_mas_suspensas = tupla_todo_aprobado + estadisticas_con_3_o_mas_suspensas
    contexto={
        "titulo":"Estadisticas evaluacion {0}".format(evaluacion),
        "num_eval":evaluacion,
        "estadisticas_totales":estadisticas_completas,
        "estadisticas_con_4_o_mas":estadisticas_con_4_o_mas_suspensas,
        "estadisticas_con_3_o_mas":estadisticas_con_3_o_mas_suspensas,
        "total_alumnos":total_alumnos
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
                if c.sin_matricula:
                    notas.append("Sin matric")
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