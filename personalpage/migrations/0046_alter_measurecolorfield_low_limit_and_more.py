# Generated by Django 4.1 on 2022-11-13 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personalpage', '0045_alter_measurecolorfield_low_limit_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurecolorfield',
            name='low_limit',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=5, null=True, verbose_name='Нижняя граница включительно'),
        ),
        migrations.AlterField(
            model_name='measurecolorfield',
            name='upper_limit',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=5, null=True, verbose_name='Верхняя граница включительно'),
        ),
    ]
