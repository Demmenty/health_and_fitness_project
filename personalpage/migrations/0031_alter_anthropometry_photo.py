# Generated by Django 4.1 on 2022-09-12 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personalpage', '0030_anthropometry_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anthropometry',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='personalpage/img/', verbose_name='Фото'),
        ),
    ]
