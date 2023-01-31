# Generated by Django 4.1 on 2023-01-22 15:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('anthropometry', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='anthropometry',
            name='photo_access',
        ),
        migrations.CreateModel(
            name='AnthropometryPhotoAccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo_access', models.BooleanField(default=False, verbose_name='Доступ эксперта к фото')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]