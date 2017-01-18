# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.auth.models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('day', models.IntegerField()),
                ('year', models.IntegerField()),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Presence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('beg', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('group', models.ForeignKey(to='app.Group', on_delete=django.db.models.deletion.PROTECT)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, to=settings.AUTH_USER_MODEL, auto_created=True, primary_key=True, serialize=False)),
                ('classe', models.CharField(max_length=10)),
                ('group', models.ForeignKey(to='app.Group', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'verbose_name': 'user',
                'abstract': False,
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='presence',
            name='session',
            field=models.ForeignKey(to='app.Session', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='presence',
            name='student',
            field=models.ForeignKey(to='app.Student', on_delete=django.db.models.deletion.PROTECT),
        ),
    ]
