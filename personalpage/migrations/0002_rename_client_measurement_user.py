# Generated by Django 4.1 on 2022-08-13 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personalpage', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='measurement',
            old_name='client',
            new_name='user',
        ),
    ]
