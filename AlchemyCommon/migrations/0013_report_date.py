# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-26 14:48
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('AlchemyCommon', '0012_auto_20160923_2110'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='date',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 9, 26, 14, 48, 35, 114061, tzinfo=utc)),
            preserve_default=False,
        ),
    ]