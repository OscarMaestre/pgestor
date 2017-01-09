from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_init
# Create your models here.

def transponer(cadena, clave, sumar=True):
    pos_clave=0
    cad_devuelta=""
    longitud_clave = len(clave)
    numero_cadena=[]
    numeros_despues=[]
    numero_clave=[]
    for i in range(0, len(cadena)):
        simbolo=cadena[i]
        o_simbolo=ord(cadena[i])
        numero_cadena.append ( o_simbolo )
        despl=ord(clave[pos_clave])
        numero_clave.append(despl)
        if sumar:
            nuevo_simbolo=(o_simbolo + despl ) % 255
            numeros_despues.append(nuevo_simbolo)
            
        else :
            nuevo_simbolo=(o_simbolo - despl ) % 255
            numeros_despues.append(nuevo_simbolo)
            
            
        cad_devuelta += chr(nuevo_simbolo)
        pos_clave = ( pos_clave + 1 ) % longitud_clave
    return cad_devuelta


def cifrar(cadena, clave):
    
    return transponer ( cadena, clave, True)

def descifrar(cadena, clave):
    return transponer ( cadena, clave, False)


    
class Grupo(models.Model):
    nombre  =   models.CharField(max_length=8)    
    
    def __str__(self):
        return self.nombre

@receiver(pre_save, sender=Grupo)
def almacenar_grupo(sender, **kwargs):
    instancia=kwargs["instance"]
    nombre=instancia.nombre
    nombre_cifrado=cifrar(nombre, "1234")
    print (nombre, nombre_cifrado)
    instancia.nombre=nombre_cifrado
    kwargs["instance"]=instancia

@receiver(post_init, sender=Grupo)
def cargar_grupo(sender, **kwargs):
    instancia=kwargs["instance"]
    nombre=instancia.nombre
    nombre_cifrado=descifrar(nombre, "1234")
    #print (nombre, nombre_cifrado)
    instancia.nombre=nombre_cifrado
    kwargs["instance"]=instancia    

    
class Modulo(models.Model):
    nombre          =   models.CharField(max_length=120)
    horas_semana    =   models.IntegerField()
    grupo           =   models.ForeignKey(Grupo)
    
    def __str__(self):
        return self.nombre
    
class Alumno(models.Model):
    apellido1           =   models.CharField(max_length=60)
    apellido2           =   models.CharField(max_length=60)
    nombre              =   models.CharField(max_length=60)
    fecha_nacimiento    =   models.DateField()
    dni                 =   models.CharField(max_length=12)
    num_exp             =   models.CharField(max_length=10)
    foto                =   models.ImageField(upload_to="fotos")
    modulos             =   models.ManyToManyField(Modulo)
    modular             =   models.BooleanField()
    inmigrante          =   models.BooleanField()