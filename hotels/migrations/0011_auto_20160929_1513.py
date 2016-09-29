# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0010_hotel_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='description',
            field=models.CharField(default=b'Not Available', max_length=1000),
        ),
    ]
