# Generated by Django 2.0.3 on 2018-07-08 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('refdata', '0008_auto_20180708_1755'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sociallink',
            options={'verbose_name': 'Ссылки на соцсети', 'verbose_name_plural': 'Ссылки на соцсети'},
        ),
        migrations.AlterField(
            model_name='sociallink',
            name='title',
            field=models.CharField(choices=[('vk', 'Vkontakte'), ('ok', 'Odnoklassniki'), ('fb', 'Facebook'), ('in', 'Instagram')], max_length=2, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='sociallink',
            name='url',
            field=models.URLField(max_length=50, verbose_name='Ссылка'),
        ),
    ]