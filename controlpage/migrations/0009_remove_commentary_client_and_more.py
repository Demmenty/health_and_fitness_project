# Generated by Django 4.1 on 2023-01-24 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controlpage', '0008_fullclientnote'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentary',
            name='client',
        ),
        migrations.RemoveField(
            model_name='fullclientnote',
            name='client',
        ),
        migrations.DeleteModel(
            name='Clientnote',
        ),
        migrations.DeleteModel(
            name='Commentary',
        ),
        migrations.DeleteModel(
            name='FullClientnote',
        ),
    ]
