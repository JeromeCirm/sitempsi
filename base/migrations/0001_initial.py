# Generated by Django 4.0.3 on 2022-08-04 16:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_demande', models.DateField(blank=True, default=None, null=True)),
                ('csrf_token', models.TextField(blank=True, default=None, null=True)),
                ('en_attente_confirmation', models.BooleanField(blank=True, default=True)),
                ('reinitialisation_password', models.BooleanField(blank=True, default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]