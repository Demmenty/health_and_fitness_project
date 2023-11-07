# Generated by Django 4.2.5 on 2023-10-06 08:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("client", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="health",
            name="client",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Клиент",
            ),
        ),
        migrations.AddField(
            model_name="changelog",
            name="client",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Клиент",
            ),
        ),
    ]
