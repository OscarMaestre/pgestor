from django.contrib import admin

# Register your models here.

from .models import Alumno, Grupo, Modulo

admin.site.register(Alumno)
admin.site.register(Grupo)
admin.site.register(Modulo)