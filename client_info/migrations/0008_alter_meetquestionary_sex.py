# Generated by Django 4.1 on 2023-02-18 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client_info', '0007_meetquestionary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetquestionary',
            name='sex',
            field=models.CharField(choices=[('M', 'Мужской'), ('F', 'Женский'), ('?', 'Другой'), ('None', None)], max_length=4, verbose_name='Биологический пол'),
        ),
    ]