# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-31 03:07
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator()])),
                ('phone', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('address', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CustomersType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customers_type_image', models.ImageField(upload_to='customers_type_image')),
                ('customer_title', models.CharField(max_length=255)),
                ('customer_description', models.CharField(max_length=1024)),
                ('customer_code', models.CharField(max_length=5)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_customer', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('code', models.CharField(max_length=10, null=True, unique=True)),
                ('status', models.CharField(default='unconfirmed', max_length=25)),
                ('validation_key', models.CharField(max_length=30, null=True)),
                ('customer_details', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reservation.CustomerDetails')),
                ('customer_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reservation.CustomersType')),
            ],
        ),
        migrations.CreateModel(
            name='ServicesType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_type_image', models.ImageField(upload_to='services_type_image')),
                ('service_title', models.CharField(max_length=255)),
                ('service_description', models.CharField(max_length=1024)),
                ('session_time_length', models.DecimalField(decimal_places=2, max_digits=4, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(9.0)])),
                ('service_code', models.CharField(max_length=5)),
                ('service_note', models.CharField(max_length=1024, null=True)),
                ('service_fee', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('for_family', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('available_manpower', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('remain_mainpower', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('capacity', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='orders',
            name='service_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reservation.ServicesType'),
        ),
        migrations.AddField(
            model_name='orders',
            name='time_slot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reservation.TimeSlot'),
        ),
        migrations.AddField(
            model_name='orders',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='customerstype',
            name='available_service',
            field=models.ManyToManyField(to='reservation.ServicesType'),
        ),
    ]
