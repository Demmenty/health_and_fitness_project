# Generated by Django 4.0.6 on 2022-08-22 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personalpage', '0017_alter_questionary_parameter11_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionary',
            name='norm_pressure',
            field=models.CharField(default=10, max_length=100, verbose_name='Знаете ли Вы свое обычное артериальное давление?'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questionary',
            name='parameter410',
            field=models.TextField(default=1, verbose_name='Принимаете ли Вы в настоящее время лекарства?'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questionary',
            name='parameter411',
            field=models.CharField(default=1, max_length=100, verbose_name='Беременны ли Вы?'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questionary',
            name='parameter412',
            field=models.CharField(default=1, max_length=255, verbose_name='Были ли у Вас роды в последние 6 месяцев?'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questionary',
            name='parameter413',
            field=models.TextField(default=1, verbose_name='Есть ли у Вас заболевания, не упомянутые в этой анкете?'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questionary',
            name='parameter414',
            field=models.TextField(default=1, verbose_name='Соблюдаете ли Вы диету?'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questionary',
            name='parameter415',
            field=models.TextField(default=1, verbose_name='Были ли у Вас в прошлом занятия, связанные с двигательной активностью (спорт, фитнес, танцы, йога и пр.)?'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questionary',
            name='parameter42',
            field=models.CharField(default=1, max_length=100, verbose_name='Имеются ли у Вас изменения нормального уровня глюкозы в крови?'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questionary',
            name='parameter43',
            field=models.CharField(default=1, max_length=255, verbose_name='Имеются ли у Вас заболевания мочевыделительной системы?'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questionary',
            name='parameter44',
            field=models.CharField(default=1, max_length=255, verbose_name='Имеются ли у Вас заболевания дыхательной системы?'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questionary',
            name='parameter45',
            field=models.CharField(default=1, max_length=255, verbose_name='Имеются ли у Вас заболевания пищеварительной системы?'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questionary',
            name='parameter46',
            field=models.CharField(default=1, max_length=255, verbose_name='Имеются ли у Вас онкологические заболевания?'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questionary',
            name='parameter47',
            field=models.CharField(default=1, max_length=255, verbose_name='Имеются ли у Вас заболевания периферических сосудов?'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questionary',
            name='parameter48',
            field=models.TextField(default=1, verbose_name='Были ли у Вас травмы и хирургические операции?'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questionary',
            name='parameter49',
            field=models.CharField(default=1, max_length=255, verbose_name='Имеются ли у Вас остеопороз, проблемы со спиной и суставами?'),
            preserve_default=False,
        ),
    ]
