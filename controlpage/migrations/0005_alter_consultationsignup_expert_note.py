# Generated by Django 4.1 on 2022-12-04 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controlpage', '0004_remove_consultationsignup_expert_comment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultationsignup',
            name='expert_note',
            field=models.TextField(blank=True, default='', verbose_name='Заметка'),
        ),
    ]
