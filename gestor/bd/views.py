#coding=utf-8
from django.shortcuts import render
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