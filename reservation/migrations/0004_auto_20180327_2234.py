# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-27 14:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0003_auto_20180325_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='code',
            field=models.CharField(max_length=15, null=True, unique=True),
        ),
    ]
