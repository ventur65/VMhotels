# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0007_hotel_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='city',
            field=models.CharField(default=b'', max_length=50),
        ),
    ]
