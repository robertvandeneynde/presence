# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='presence',
            name='session',
        ),
        migrations.RemoveField(
            model_name='presence',
            name='student',
        ),
        migrations.AddField(
            model_name='session',
            name='presents',
            field=models.ManyToManyField(to='app.Student'),
        ),
        migrations.DeleteModel(
            name='Presence',
        ),
    ]
