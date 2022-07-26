# Generated by Django 4.0 on 2022-08-11 17:55

from django.db import migrations, models
import gestionmenu.models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionmenu', '0003_alter_menu_gestionnaires_alter_menu_groupes_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fichier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, default='', max_length=5000)),
                ('fichier', models.FileField(blank=True, null=True, upload_to=gestionmenu.models.Fichier.uploadpath)),
                ('nomfichier', models.CharField(blank=True, max_length=100, null=True)),
                ('ordre', models.IntegerField()),
                ('menu', models.IntegerField()),
            ],
            options={
                'ordering': ['-ordre'],
            },
        ),
    ]
