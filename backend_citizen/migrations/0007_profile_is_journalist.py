# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-08-04 20:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_citizen', '0006_profile_is_organization'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_journalist',
            field=models.BooleanField(default=False),
        ),
    ]
