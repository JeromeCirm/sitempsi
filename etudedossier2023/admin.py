from django.contrib import admin
from .models import GestionDossier2023,SauvegardeSelection2023

class GestionDossier2023Admin(admin.ModelAdmin):
    list_display=('fichier_initial',)

class SauvegardeSelection2023Admin(admin.ModelAdmin):
    list_display=('user','valeur','ordre','boursier','pasexpert')

admin.site.register(SauvegardeSelection2023,SauvegardeSelection2023Admin)
admin.site.register(GestionDossier2023,GestionDossier2023Admin)