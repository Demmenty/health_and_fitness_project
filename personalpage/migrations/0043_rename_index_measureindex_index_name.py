# Generated by Django 4.1 on 2022-11-13 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personalpage', '0042_alter_measurecolorfield_low_limit_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='measureindex',
            old_name='index',
            new_name='index_name',
        ),
    ]