# Generated by Django 4.1 on 2023-02-12 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client_info', '0002_alter_healthquestionary_parameter416_exp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='healthquestionary',
            name='parameter416_exp',
            field=models.CharField(default='no', max_length=200, verbose_name='Cтаж занятий'),
        ),
    ]
