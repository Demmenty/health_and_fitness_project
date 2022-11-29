# Generated by Django 4.1 on 2022-11-19 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personalpage', '0050_usersettings_discord_usersettings_facebook_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersettings',
            name='preferred_contact',
            field=models.CharField(choices=[('TG', 'Telegram'), ('WA', 'Whatsapp'), ('DC', 'Discord'), ('SK', 'Skype'), ('VK', 'Vkontakte'), ('FB', 'Facebook'), ('No', 'не выбрано')], default='No', max_length=2, verbose_name='Предпочтительный способ связи'),
        ),
    ]