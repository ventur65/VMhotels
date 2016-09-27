# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0006_auto_20160831_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='city',
            field=models.CharField(default='Rome', max_length=50),
            preserve_default=False,
        ),
    ]
