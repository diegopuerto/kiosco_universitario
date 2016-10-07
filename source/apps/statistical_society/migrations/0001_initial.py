# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('DaneUsers', '0002_auto_20160408_1648'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatisticalSocietyUserPreference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('use_of_info', models.CharField(max_length=120, verbose_name='use of statistical information')),
                ('suscription_media', models.CharField(max_length=120, verbose_name='suscription media')),
                ('want_cell_messages', models.BooleanField(default=False, max_length=50, verbose_name='Wants receive cell messages')),
                ('want_email_messages', models.BooleanField(default=False, max_length=50, verbose_name='Wants receive email messages')),
                ('pib_info', models.BooleanField(default=False, max_length=50, verbose_name='gross domestic product')),
                ('ipc_info', models.BooleanField(default=False, max_length=50, verbose_name="consumer's price index")),
                ('ipp_info', models.BooleanField(default=False, max_length=50, verbose_name="producer's price index")),
                ('workforce_info', models.BooleanField(default=False, max_length=50, verbose_name='Global Participation Rate / Rate occupation / Unemployment Rate / percent of working age population')),
                ('imports_info', models.BooleanField(default=False, max_length=50, verbose_name='imports')),
                ('exports_info', models.BooleanField(default=False, max_length=50, verbose_name='exports')),
                ('mmcm_info', models.BooleanField(default=False, max_length=50, verbose_name='sample monthly retail')),
                ('mmm_info', models.BooleanField(default=False, max_length=50, verbose_name='monthly manufacturing sample')),
            ],
        ),
        migrations.CreateModel(
            name='StatisticalSocietyMember',
            fields=[
            ],
            options={
                'verbose_name': 'Statistical Society Member',
                'proxy': True,
                'verbose_name_plural': 'Statistical Society Members',
            },
            bases=('DaneUsers.basicdaneuser',),
        ),
        migrations.CreateModel(
            name='StatisticalSocietyMemberEmail',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('DaneUsers.basicdaneuser',),
        ),
        migrations.AddField(
            model_name='statisticalsocietyuserpreference',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
