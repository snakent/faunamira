# Generated by Django 2.0.3 on 2018-06-30 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animal', '0014_animal_viewed'),
        ('blog', '0004_auto_20180412_0843'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='animals',
            field=models.ManyToManyField(to='animal.Animal'),
        ),
    ]
