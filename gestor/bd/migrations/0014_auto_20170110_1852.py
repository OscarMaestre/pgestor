# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-10 18:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bd', '0013_auto_20170110_1840'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alumno',
            old_name='emancipada',
            new_name='esta_emancipado',
        ),
    ]