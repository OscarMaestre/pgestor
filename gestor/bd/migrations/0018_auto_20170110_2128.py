# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-10 21:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bd', '0017_auto_20170110_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calificacion',
            name='apro',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='calificacion',
            name='conv',
            field=models.NullBooleanField(),
        ),
    ]
