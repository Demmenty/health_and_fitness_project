# Generated by Django 4.1 on 2022-11-19 19:23

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
            name='Commentary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today, verbose_name='Дата')),
                ('general', models.TextField(blank=True, default='', verbose_name='Общее')),
                ('measurements', models.TextField(blank=True, default='', verbose_name='Измерения')),
                ('nutrition', models.TextField(blank=True, default='', verbose_name='Питание')),
                ('workout', models.TextField(blank=True, default='', verbose_name='Тренировки')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
