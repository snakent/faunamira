# Generated by Django 2.0.3 on 2018-03-27 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animal', '0007_auto_20180327_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='animal',
            name='status',
            field=models.CharField(blank=True, choices=[('B', 'Boy'), ('G', 'Girl')], max_length=1, null=True, verbose_name='Status'),
        ),
    ]