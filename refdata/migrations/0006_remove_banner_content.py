# Generated by Django 2.0.3 on 2018-04-16 14:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('refdata', '0005_banner_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banner',
            name='content',
        ),
    ]
