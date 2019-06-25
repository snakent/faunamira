# Generated by Django 2.0.3 on 2018-06-20 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0012_auto_20180416_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='profile/avatar', verbose_name='Аватар'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='birthday',
            field=models.DateField(blank=True, null=True, verbose_name='Дата рождения'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='refdata.City', verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Men'), ('W', 'Woman')], max_length=1, null=True, verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='hobbies',
            field=models.ManyToManyField(blank=True, to='userprofile.ProfileHobby', verbose_name='Интересы'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='info',
            field=models.TextField(blank=True, null=True, verbose_name='Обо мне'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='profileabout',
            name='about_me',
            field=models.TextField(blank=True, verbose_name='Обо мне'),
        ),
        migrations.AlterField(
            model_name='profileabout',
            name='find',
            field=models.CharField(blank=True, choices=[('M', 'Мужчина'), ('W', 'Женщина')], max_length=2, verbose_name='Я ищу'),
        ),
        migrations.AlterField(
            model_name='profileabout',
            name='purpose',
            field=models.CharField(blank=True, choices=[('CMN', 'Общение'), ('FNF', 'Дружба'), ('GOD', 'Свидание')], max_length=3, verbose_name='Цель знакомства'),
        ),
    ]