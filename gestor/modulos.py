#!/usr/bin/env python3

from utilidades.basedatos.Configurador import Configurador
from constantes import *
configurador=Configurador(".")

configurador.activar_configuracion("gestor.settings")



from bd.models import *


if __name__ == '__main__':
    dam1=Grupo(nombre="DAM1")
    dam1.save()
    m1=Modulo(nombre=LENGUAJES_DE_MARCAS, horas_semana=4, grupo=dam1, horas_anuales=100)
    m1.save()
    m2=Modulo(nombre=PROGRAMACION, horas_semana=6, grupo=dam1, horas_anuales=100)
    m2.save()
    m2=Modulo(nombre=BASES_DE_DATOS, horas_semana=6, grupo=dam1, horas_anuales=100)
    m2.save()
    m2=Modulo(nombre=SISTEMAS_OPERATIVOS, horas_semana=7, grupo=dam1, horas_anuales=100)
    m2.save()
    m2=Modulo(nombre=ENTORNOS_DE_DESARROLLO, horas_semana=3, grupo=dam1, horas_anuales=100)
    m2.save()
    m2=Modulo(nombre=INGLES, horas_semana=3, grupo=dam1, horas_anuales=100)
    m2.save()
    m2=Modulo(nombre=FOL, horas_semana=6, grupo=dam1, horas_anuales=100)
    m2.save()
    

