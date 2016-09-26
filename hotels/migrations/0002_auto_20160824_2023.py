# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rseates', models.IntegerField(default=1)),
                ('number', models.IntegerField(default=1)),
                ('description', models.CharField(max_length=300)),
                ('cost', models.FloatField()),
                ('hotel', models.ForeignKey(to='hotels.Hotel')),
            ],
        ),
        migrations.RemoveField(
            model_name='chamber',
            name='hotel',
        ),
        migrations.DeleteModel(
            name='Chamber',
        ),
    ]
