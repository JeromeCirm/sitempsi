from django.contrib import admin
from .models import GestionDossier2026,SauvegardeSelection2026

class GestionDossier2026Admin(admin.ModelAdmin):
    list_display=('fichier_initial',)

class SauvegardeSelection2026Admin(admin.ModelAdmin):
    list_display=('user','valeur','ordre','boursier','pasexpert')

admin.site.register(SauvegardeSelection2026,SauvegardeSelection2026Admin)
admin.site.register(GestionDossier2026,GestionDossier2026Admin)