# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-25 11:15
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0002_auto_20180131_0308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerdetails',
            name='phone',
            field=models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(message='\u884c\u52d5\u96fb\u8a71\u865f\u78bc\u683c\u5f0f\u5fc5\u9808\u662f\u300c0910123456\u300d\u6216\u300c+886910123456\u300d\uff0c\u8acb\u518d\u6b21\u78ba\u8a8d\u96fb\u8a71\u865f\u78bc\u3002', regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]
