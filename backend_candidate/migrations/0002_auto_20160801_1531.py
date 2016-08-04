# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-08-01 15:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0025_auto_20160701_1735'),
        ('backend_candidate', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CandidacyContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail', models.EmailField(max_length=254)),
                ('times_email_has_been_sent', models.IntegerField(default=0)),
                ('used_by_candidate', models.BooleanField(default=False)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to='elections.Candidate')),
            ],
        ),
        migrations.AlterField(
            model_name='candidacy',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidacies', to=settings.AUTH_USER_MODEL),
        ),
    ]