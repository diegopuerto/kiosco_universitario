# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-11 03:01
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('DaneUsers', '0006_auto_20161003_2312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicdaneuser',
            name='key_expires',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 18, 3, 1, 28, 482076, tzinfo=utc)),
        ),
    ]