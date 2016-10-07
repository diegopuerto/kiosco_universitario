# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import libs.django_smart_selects.smart_selects.db_fields
import django_countries.fields
from django.utils.timezone import utc
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alias', models.CharField(max_length=120, verbose_name='Alias')),
                ('name', models.CharField(max_length=240, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Activity Type',
                'verbose_name_plural': 'Activity Types',
            },
        ),
        migrations.CreateModel(
            name='AgeRange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alias', models.CharField(max_length=120, verbose_name='Alias')),
                ('name', models.CharField(max_length=240, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Age Range',
                'verbose_name_plural': 'Age Ranges',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alias', models.CharField(max_length=120, verbose_name='Alias')),
                ('name', models.CharField(max_length=240, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'City',
                'verbose_name_plural': 'Cities',
            },
        ),
        migrations.CreateModel(
            name='Departament',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alias', models.CharField(max_length=120, verbose_name='Alias')),
                ('name', models.CharField(max_length=240, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Departament',
            },
        ),
        migrations.CreateModel(
            name='DisabilityType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alias', models.CharField(max_length=120, verbose_name='Alias')),
                ('name', models.CharField(max_length=240, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Disability Type',
                'verbose_name_plural': 'Disability Types',
            },
        ),
        migrations.CreateModel(
            name='EducationalType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alias', models.CharField(max_length=120, verbose_name='Alias')),
                ('name', models.CharField(max_length=240, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Educational Type',
                'verbose_name_plural': 'Educational Types',
            },
        ),
        migrations.CreateModel(
            name='IdType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alias', models.CharField(max_length=120, verbose_name='Alias')),
                ('name', models.CharField(max_length=240, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'ID Type',
                'verbose_name_plural': 'ID Types',
            },
        ),
        migrations.CreateModel(
            name='ProfessionalType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alias', models.CharField(max_length=120, verbose_name='Alias')),
                ('name', models.CharField(max_length=240, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Professional Type',
                'verbose_name_plural': 'Professional Types',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_doc', models.CharField(max_length=30, unique=True, null=True, verbose_name='ID document', blank=True)),
                ('cellphone', models.CharField(max_length=120, null=True, verbose_name='Cellphone', blank=True)),
                ('phone', models.CharField(max_length=120, null=True, verbose_name='phone', blank=True)),
                ('gender', models.NullBooleanField(default=None, verbose_name='Gender', choices=[(None, 'Select gender'), (True, 'Male'), (False, 'Female')])),
                ('country_of_residence', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('alternative_mail', models.EmailField(max_length=254, unique=True, null=True, verbose_name='alternative mail', blank=True)),
                ('activity', models.ForeignKey(blank=True, to='DaneUsers.ActivityType', null=True)),
                ('age_range', models.ForeignKey(blank=True, to='DaneUsers.AgeRange', null=True)),
                ('city', libs.django_smart_selects.smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'departament', to='DaneUsers.City', chained_field=b'departament', auto_choose=True)),
                ('departament', models.ForeignKey(to='DaneUsers.Departament')),
                ('disability', models.ForeignKey(blank=True, to='DaneUsers.DisabilityType', null=True)),
                ('education', models.ForeignKey(blank=True, to='DaneUsers.EducationalType', null=True)),
                ('id_type', models.ForeignKey(blank=True, to='DaneUsers.IdType', null=True)),
                ('profession', models.ForeignKey(blank=True, to='DaneUsers.ProfessionalType', null=True)),
            ],
            options={
                'verbose_name': 'User Profile',
                'verbose_name_plural': 'User Profiles',
            },
        ),
        migrations.CreateModel(
            name='BasicDaneUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name='email address', db_index=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=50, null=True, verbose_name='Names')),
                ('last_name', models.CharField(max_length=50, null=True, verbose_name='Surnames')),
                ('_is_staff', models.BooleanField(default=False, verbose_name='Is Staff')),
                ('_is_active', models.BooleanField(default=True, verbose_name='Is Staff')),
                ('key_expires', models.DateTimeField(default=datetime.datetime(2016, 4, 15, 21, 47, 47, 975000, tzinfo=utc))),
                ('is_confirmed', models.BooleanField(default=False, verbose_name='Is Confirmed')),
                ('activation_key', models.CharField(max_length=40, null=True)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
            },
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='city',
            name='departament',
            field=models.ForeignKey(to='DaneUsers.Departament'),
        ),
    ]
