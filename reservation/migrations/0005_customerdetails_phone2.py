# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-11 09:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0004_auto_20180327_2234'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerdetails',
            name='phone2',
            field=models.CharField(blank=True, max_length=16),
        ),
    ]