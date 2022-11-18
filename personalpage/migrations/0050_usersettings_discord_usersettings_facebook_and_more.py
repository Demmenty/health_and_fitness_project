# Generated by Django 4.1 on 2022-11-18 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personalpage', '0049_alter_measurecolorfield_low_limit_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersettings',
            name='discord',
            field=models.URLField(blank=True, max_length=250, null=True, verbose_name='Discord'),
        ),
        migrations.AddField(
            model_name='usersettings',
            name='facebook',
            field=models.URLField(blank=True, max_length=250, null=True, verbose_name='Facebook'),
        ),
        migrations.AddField(
            model_name='usersettings',
            name='preferred_contact',
            field=models.CharField(choices=[('TG', 'Telegram'), ('WA', 'Whatsapp'), ('DC', 'Discord'), ('SK', 'Skype'), ('VK', 'Vkontakte'), ('FB', 'Facebook'), ('', '')], default='', max_length=2, verbose_name='Предпочтительный способ связи'),
        ),
        migrations.AddField(
            model_name='usersettings',
            name='skype',
            field=models.URLField(blank=True, max_length=250, null=True, verbose_name='Skype'),
        ),
        migrations.AddField(
            model_name='usersettings',
            name='telegram',
            field=models.URLField(blank=True, max_length=250, null=True, verbose_name='Telegram'),
        ),
        migrations.AddField(
            model_name='usersettings',
            name='vkontakte',
            field=models.URLField(blank=True, max_length=250, null=True, verbose_name='Vkontakte'),
        ),
        migrations.AddField(
            model_name='usersettings',
            name='whatsapp',
            field=models.URLField(blank=True, max_length=250, null=True, verbose_name='Whatsapp'),
        ),
        migrations.AlterField(
            model_name='measurecolorfield',
            name='low_limit',
            field=models.DecimalField(blank=True, decimal_places=1, default=None, max_digits=5, null=True, verbose_name='Нижняя граница включительно'),
        ),
        migrations.AlterField(
            model_name='measurecolorfield',
            name='upper_limit',
            field=models.DecimalField(blank=True, decimal_places=1, default=None, max_digits=5, null=True, verbose_name='Верхняя граница включительно'),
        ),
    ]