from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Alumno)
admin.site.register(Grupo)
admin.site.register(Modulo)
admin.site.register(Calificacion)