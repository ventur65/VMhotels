# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0003_auto_20160830_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='address',
            field=models.CharField(unique=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='email',
            field=models.EmailField(unique=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='name',
            field=models.CharField(unique=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='tel',
            field=models.PositiveIntegerField(unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='room',
            unique_together=set([('hotel', 'number')]),
        ),
    ]
