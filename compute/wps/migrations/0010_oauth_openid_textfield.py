# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-25 20:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wps', '0009_oauth2_primary_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oauth2',
            name='openid',
            field=models.TextField(),
        ),
    ]
