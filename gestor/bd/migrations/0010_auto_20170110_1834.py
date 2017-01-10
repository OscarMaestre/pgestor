# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-10 18:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bd', '0009_alumno_repetidor'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='alumno',
            options={'ordering': ['apellidos', 'nombre']},
        ),
        migrations.AddField(
            model_name='alumno',
            name='comentarios',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]