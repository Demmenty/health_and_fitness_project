# Generated by Django 4.1 on 2022-08-24 10:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('personalpage', '0020_questionary_confirm_questionary_parameter417_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FatSecretEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_token', models.CharField(blank=True, max_length=255, null=True)),
                ('oauth_token', models.CharField(blank=True, max_length=255, null=True)),
                ('oauth_token_secret', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
