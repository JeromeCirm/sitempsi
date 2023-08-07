from django.contrib import admin
from .models import GestionDossier2021,SauvegardeSelection2021

class GestionDossier2021Admin(admin.ModelAdmin):
    list_display=('fichier_initial',)

class SauvegardeSelection2021Admin(admin.ModelAdmin):
    list_display=('user','valeur','ordre','boursier','pasexpert')

admin.site.register(SauvegardeSelection2021,SauvegardeSelection2021Admin)
admin.site.register(GestionDossier2021,GestionDossier2021Admin)