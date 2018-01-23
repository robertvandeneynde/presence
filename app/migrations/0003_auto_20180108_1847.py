# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-08 18:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20170118_2125'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='other_year',
            field=models.ManyToManyField(blank=True, related_name='_student_other_year_+', to='app.Student'),
        ),
        migrations.AlterField(
            model_name='session',
            name='presents',
            field=models.ManyToManyField(blank=True, to='app.Student'),
        ),
    ]