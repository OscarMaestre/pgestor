# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-10 21:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bd', '0014_auto_20170110_1852'),
    ]

    operations = [
        migrations.AddField(
            model_name='calificacion',
            name='eval',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
