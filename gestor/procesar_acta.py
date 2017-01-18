#!/usr/bin/env python3
#coding=utf-8

import sys
import re
from utilidades.ficheros.ProcesadorPDF import ProcesadorPDF
from utilidades.basedatos.Configurador import Configurador


configurador=Configurador(".")
configurador.activar_configuracion("gestor.settings")

from bd.models import Alumno, Modulo, Calificacion
from constantes import *
from django.db import transaction
re_nombre="(?P<nombre>[A-Za-zÁÉÍÓÚáéíóúÑñ\- ]+, [A-Za-zÁÉÍÓÚáéíóúÑñ\- ]+)"
re_calificaciones="(CONV|APRO|[0-9]+)"

expr_regular=re.compile(re_nombre)

INI_ALUMNO=36
FIN_ALUMNO=86

#Cargamos los modulos en el orden en que salen en el acta
try:
    print()
    print("*"*50)
    print("Por favor comprueba que las notas y los nombres de alumnos están alineados")
    print("*"*50)
    print()
    ssii=Modulo.objects.get( nombre=SISTEMAS_OPERATIVOS     )
    bbdd=Modulo.objects.get( nombre=BASES_DE_DATOS          )
    prog=Modulo.objects.get( nombre=PROGRAMACION            )
    llmm=Modulo.objects.get( nombre=LENGUAJES_DE_MARCAS     )
    eedd=Modulo.objects.get( nombre=ENTORNOS_DE_DESARROLLO  )
    ingl=Modulo.objects.get( nombre=INGLES                  )
    fol =Modulo.objects.get( nombre=FOL                     )
    #Aqui se indican las posiciones de inicio y fin de cada campo de calificacion
    campos=[ (96, 105, ssii),  (108,118, bbdd), (121, 129, prog),
                (130, 140, llmm), (144, 154, eedd),
                (154, 164, fol), (164, 178, ingl)]
except:
    print("Error:No se han podido cargar los modulos")
    sys.exit(-1)

def get_apellido_alumno(nombre):
    #Buscamos la coma
    pos_coma=nombre.find(",")
    if pos_coma==-1:
        print ("ERROR, no se encontro el apellido en "+nombre)
        return
    else:
        return nombre[:pos_coma]
def procesar_posible_alumno(linea):
    evaluacion=int(sys.argv[2])
    modelo_alumno=get_alumno(linea)
    if modelo_alumno==None:
        return
    print(modelo_alumno)
    for tupla in campos:
        ini=tupla[0]
        fin=tupla[1]
        modulo_asociado=tupla[2]
        nota=linea[ini:fin].strip()
        if nota=="":
            c=Calificacion(alumno=modelo_alumno, sin_matricula=True, ev=evaluacion, modulo=modulo_asociado)
            c.save()
            continue
        if nota=="CONV":
            c=Calificacion(alumno=modelo_alumno, conv=True, ev=evaluacion, modulo=modulo_asociado)
            c.save()
            continue
        if nota=="APRO":
            c=Calificacion(alumno=modelo_alumno, apro=True, ev=evaluacion, modulo=modulo_asociado)
            c.save()
            continue
        num_nota=int(nota)
        if num_nota>=0 and num_nota<=10:
            c=Calificacion(alumno=modelo_alumno, conv=False, apro=False,
                           ev=evaluacion, calificacion=num_nota, modulo=modulo_asociado)
            c.save()
            
        else:
            raise ValueError("La nota no es numerica ni APRO ni CONV-->"+nota)
    
    
def get_alumno(linea):
    nombre_alumno=linea[INI_ALUMNO:FIN_ALUMNO].strip()
    apellidos_leidos=get_apellido_alumno(nombre_alumno)
    try:
        modelo=Alumno.objects.get(apellidos=apellidos_leidos)
    except:
        print("Error:No hay apellido en "+linea.strip())
        return None
    #print(modelo)
    return modelo
    
def procesar_acta(fichero, num_eval):
    print ("Acta:"+fichero, "Evaluacion:"+num_eval)
    procesador=ProcesadorPDF()
    nombre_fich_txt=procesador.convertir_a_txt(fichero)
    procesador.abrir_fichero_txt(nombre_fich_txt)
    linea=procesador.get_linea_actual()
    while(not procesador.eof()):
        (ini, fin, texto)=procesador.linea_contiene_patron(expr_regular, linea)
        if ini!=procesador.PATRON_NO_ENCONTRADO:
            #print(texto.strip())
            procesar_posible_alumno(linea)
        procesador.siguiente_fila()
        linea=procesador.get_linea_actual()
if __name__ == '__main__':
    #Calificacion.objects.filter(ev=sys.argv[2]).delete()
    with transaction.atomic():
        procesar_acta(sys.argv[1], sys.argv[2])