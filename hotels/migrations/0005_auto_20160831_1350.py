# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import hotels.models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0004_auto_20160830_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='image',
            field=models.ImageField(height_field=50, width_field=50, null=True, upload_to=hotels.models.path_to_hotel_image),
        ),
        migrations.AddField(
            model_name='room',
            name='image',
            field=models.ImageField(height_field=50, width_field=50, null=True, upload_to=hotels.models.path_to_room_image),
        ),
    ]
