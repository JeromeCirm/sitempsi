# Generated by Django 4.0 on 2022-08-27 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('gestionmenu', '0016_progcollemath'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotesColles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.IntegerField()),
                ('semaine', models.IntegerField()),
                ('colleur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
                ('eleve', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_requests_created', to='auth.user')),
            ],
        ),
    ]
