# Generated by Django 4.0 on 2022-08-11 19:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestionmenu', '0006_alter_fichier_menu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fichier',
            name='menu',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gestionmenu.menu'),
        ),
    ]