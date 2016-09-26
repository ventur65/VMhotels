# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0002_auto_20160824_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='tel',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='room',
            name='number',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='room',
            name='rseates',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
