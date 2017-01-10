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

#@receiver(pre_save, sender=Grupo)
def almacenar_grupo(sender, **kwargs):
    instancia=kwargs["instance"]
    nombre=instancia.nombre
    nombre_cifrado=cifrar(nombre, "1234")
    print (nombre, nombre_cifrado)
    instancia.nombre=nombre_cifrado
    kwargs["instance"]=instancia

#@receiver(post_init, sender=Grupo)
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
    horas_anuales   =   models.IntegerField()
    
    def __str__(self):
        return self.nombre
    
class Alumno(models.Model):
    dni                 =   models.CharField(max_length=12, blank=True)
    apellidos           =   models.CharField(max_length=140)
    nombre              =   models.CharField(max_length=60)
    fecha_nacimiento    =   models.DateField(blank=True, null=True)
    email               =   models.EmailField(blank=True)
    dir_postal          =   models.CharField(max_length=140, blank=True)
    tlf_urgencia_1      =   models.CharField(max_length=12, blank=True)
    tlf_urgencia_2      =   models.CharField(max_length=12, blank=True)
    num_exp             =   models.CharField(max_length=10, blank=True)
    foto                =   models.ImageField(upload_to="fotos", blank=True)
    matricula           =   models.ManyToManyField(Modulo, related_name="matriculas")
    convalidaciones     =   models.ManyToManyField(Modulo, related_name="convalidaciones", blank=True)
    mods_aprobados      =   models.ManyToManyField(Modulo, related_name="aprobados", blank=True)
    modular             =   models.BooleanField(blank=True)
    inmigrante          =   models.BooleanField(blank=True)
    repetidor           =   models.BooleanField(blank=True)
    emancipada          =   models.BooleanField(blank=True)
    comentarios         =   models.TextField(blank=True)
    
    
    def __str__(self):
        return self.apellidos + " " + self.nombre
    
    class Meta:
        ordering = ["apellidos", "nombre"]
    
class Calificacion(models.Model):
    alumno      =       models.ForeignKey ( Alumno )
    calificacion=       models.IntegerField(blank=True)
    conv        =       models.BooleanField()
    apro        =       models.BooleanField()
    