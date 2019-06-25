# Generated by Django 2.0.3 on 2018-06-29 11:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('animal', '0012_animalphoto'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnimalViewed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('animal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='animal_viewed', to='animal.Animal', verbose_name='Animal')),
                ('profile_page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='an_user_viewed', to=settings.AUTH_USER_MODEL, verbose_name='Profile_page')),
            ],
            options={
                'verbose_name_plural': 'Animals Viewed',
                'verbose_name': 'Animal Viewed',
            },
        ),
    ]
