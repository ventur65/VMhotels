# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0008_auto_20160927_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='address',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterUniqueTogether(
            name='hotel',
            unique_together=set([('city', 'address')]),
        ),
    ]
