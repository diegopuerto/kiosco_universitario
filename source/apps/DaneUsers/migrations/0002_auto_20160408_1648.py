# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('DaneUsers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicdaneuser',
            name='key_expires',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 15, 21, 48, 55, 79000, tzinfo=utc)),
        ),
    ]
