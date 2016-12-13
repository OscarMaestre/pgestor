from django.db import models

# Create your models here.


class Grupo(models.Model):
    nombre  =   models.CharField(max_length=8)
    
    def __str__(self):
        return self.nombre
    
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