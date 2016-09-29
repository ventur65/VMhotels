# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import hotels.models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0011_auto_20160929_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='description',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='image',
            field=models.ImageField(height_field=b'_height', width_field=b'_width', null=True, upload_to=hotels.models.path_to_hotel_image, blank=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='image',
            field=models.ImageField(height_field=b'_height', width_field=b'_width', null=True, upload_to=hotels.models.path_to_room_image, blank=True),
        ),
    ]
