# Generated by Django 4.1 on 2023-02-19 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client_info', '0010_meetquestionary_sleep_problems_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meetquestionary',
            name='daily_meal',
        ),
        migrations.AddField(
            model_name='meetquestionary',
            name='common_meal',
            field=models.TextField(default='...', verbose_name='5 видов пищи, кот вы едите наиболее часто и регулярно'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='meetquestionary',
            name='favorite_meal',
            field=models.TextField(default='aaa', verbose_name='5 видов пищи, которые вы считаете самыми вкусными, желанными и любимыми'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='meetquestionary',
            name='yearly_meal',
            field=models.TextField(default='a', verbose_name='5 вида пиши, кот вы едите несколько раз в год'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='meetquestionary',
            name='sex',
            field=models.CharField(choices=[('M', 'Мужской'), ('F', 'Женский'), ('?', 'Свой вариант')], max_length=1, verbose_name='Биологический пол'),
        ),
        migrations.AlterField(
            model_name='meetquestionary',
            name='weekly_meal',
            field=models.TextField(verbose_name='5 видов пищи, кот вы едите примерно раз в неделю'),
        ),
    ]