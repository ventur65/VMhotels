# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0012_auto_20160929_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='description',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='description',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
    ]
