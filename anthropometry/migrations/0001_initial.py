# Generated by Django 4.1 on 2023-01-22 10:39

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Anthropometry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today, verbose_name='Дата')),
                ('shoulder', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True, verbose_name='Плечо')),
                ('chest', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True, verbose_name='Грудь')),
                ('waist', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True, verbose_name='Талия')),
                ('belly', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True, verbose_name='Живот')),
                ('buttocks', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True, verbose_name='Ягодицы')),
                ('hip', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True, verbose_name='Бедро')),
                ('shin', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True, verbose_name='Голень')),
                ('photo_1', models.ImageField(blank=True, max_length=255, null=True, upload_to='personalpage/img/clients/%Y/%d.%m', verbose_name='Фото №1')),
                ('photo_2', models.ImageField(blank=True, max_length=255, null=True, upload_to='personalpage/img/clients/%Y/%d.%m', verbose_name='Фото №2')),
                ('photo_3', models.ImageField(blank=True, max_length=255, null=True, upload_to='personalpage/img/clients/%Y/%d.%m', verbose_name='Фото №3')),
                ('photo_access', models.BooleanField(default=False, verbose_name='Доступ эксперта к фото')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
                'get_latest_by': 'date',
            },
        ),
    ]
