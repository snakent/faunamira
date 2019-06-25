# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-14 12:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0004_profilehobby'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='hobbies',
            field=models.ManyToManyField(blank=True, to='userprofile.ProfileHobby', verbose_name='Hobbies'),
        ),
    ]