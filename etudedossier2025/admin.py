from django.contrib import admin
from .models import GestionDossier2025,SauvegardeSelection2025

class GestionDossier2025Admin(admin.ModelAdmin):
    list_display=('fichier_initial',)

class SauvegardeSelection2025Admin(admin.ModelAdmin):
    list_display=('user','valeur','ordre','boursier','pasexpert')

admin.site.register(SauvegardeSelection2025,SauvegardeSelection2025Admin)
admin.site.register(GestionDossier2025,GestionDossier2025Admin)