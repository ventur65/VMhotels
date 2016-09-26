# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chamber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rseates', models.IntegerField(default=1)),
                ('number', models.IntegerField(default=1)),
                ('description', models.CharField(max_length=300)),
                ('cost', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=1000)),
                ('email', models.EmailField(max_length=254)),
                ('tel', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='chamber',
            name='hotel',
            field=models.ForeignKey(to='hotels.Hotel'),
        ),
    ]
