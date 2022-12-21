from django.contrib import admin
from .models import GestionDossier,SauvegardeSelection

class GestionDossierAdmin(admin.ModelAdmin):
    list_display=('fichier_initial',)

class SauvegardeSelectionAdmin(admin.ModelAdmin):
    list_display=('user','valeur','ordre','boursier','pasexpert')

admin.site.register(SauvegardeSelection,SauvegardeSelectionAdmin)
admin.site.register(GestionDossier,GestionDossierAdmin)