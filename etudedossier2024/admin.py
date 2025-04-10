from django.contrib import admin
from .models import GestionDossier2024,SauvegardeSelection2024,AnciensEleves

class GestionDossier2024Admin(admin.ModelAdmin):
    list_display=('fichier_initial',)

class SauvegardeSelection2024Admin(admin.ModelAdmin):
    list_display=('user','valeur','ordre','boursier','pasexpert')

class AnciensElevesAdmin(admin.ModelAdmin):
    pass #list_display=('user','valeur','ordre','boursier','pasexpert')

admin.site.register(AnciensEleves,AnciensElevesAdmin)
admin.site.register(SauvegardeSelection2024,SauvegardeSelection2024Admin)
admin.site.register(GestionDossier2024,GestionDossier2024Admin)