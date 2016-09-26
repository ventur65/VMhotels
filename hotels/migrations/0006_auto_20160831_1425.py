# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import hotels.models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0005_auto_20160831_1350'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='rseates',
            new_name='beds',
        ),
        migrations.AlterField(
            model_name='hotel',
            name='image',
            field=models.ImageField(height_field=b'_height', width_field=b'_width', null=True, upload_to=hotels.models.path_to_hotel_image),
        ),
        migrations.AlterField(
            model_name='room',
            name='image',
            field=models.ImageField(height_field=b'_height', width_field=b'_width', null=True, upload_to=hotels.models.path_to_room_image),
        ),
    ]
