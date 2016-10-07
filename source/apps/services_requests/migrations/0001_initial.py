# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecializedChamberRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('detail', models.TextField(verbose_name='detail')),
                ('is_closed', models.BooleanField(default=False, verbose_name='Request is closed')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('from_ip', models.TextField(verbose_name='from ip')),
                ('service', models.CharField(max_length=255, verbose_name='service')),
                ('assigned_to', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Specialized Chamber Request',
                'verbose_name_plural': 'Specialized Chamber Requests',
            },
        ),
        migrations.CreateModel(
            name='StatisticalCultureRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('detail', models.TextField(verbose_name='detail')),
                ('is_closed', models.BooleanField(default=False, verbose_name='Request is closed')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('from_ip', models.TextField(verbose_name='from ip')),
                ('assigned_to', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Statistical Culture Request',
                'verbose_name_plural': 'Statistical Culture Requests',
            },
        ),
        migrations.CreateModel(
            name='StatisticalCultureService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alias', models.CharField(max_length=120, verbose_name='Alias')),
                ('name', models.CharField(max_length=240, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Statistical Culture Service',
                'verbose_name_plural': 'Statistical Culture Services',
            },
        ),
        migrations.AddField(
            model_name='statisticalculturerequest',
            name='service',
            field=models.ForeignKey(to='services_requests.StatisticalCultureService'),
        ),
        migrations.AddField(
            model_name='statisticalculturerequest',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
