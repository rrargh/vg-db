# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-02 16:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20161003_0016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ministry',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='venue',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]