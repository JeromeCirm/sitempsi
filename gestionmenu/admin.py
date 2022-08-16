from django.contrib import admin
from .models import *

class MenuAdmin(admin.ModelAdmin):
    list_display=('nom','id','parent','ordre','fonction')

class FichierAdmin(admin.ModelAdmin):
    pass

class SemainesAdmin(admin.ModelAdmin):
    list_display=('numero','date')

class CreneauxColleursAdmin(admin.ModelAdmin):
    list_display=('numero','colleur','jour','horaire','salle')

class GroupeCollesAdmin(admin.ModelAdmin):
    list_display=('numero','get_eleves')

    def get_eleves(self,obj):
        return ", ".join([x.username for x in obj.eleves.all()])

class ColloscopeAdmin(admin.ModelAdmin):
    list_display=('semaine','groupe','creneau')

class RenseignementsAdmin(admin.ModelAdmin):
    list_display=('login','année','prenomusage','nomusage')

admin.site.register(Menu,MenuAdmin)
admin.site.register(Fichier,FichierAdmin)
admin.site.register(Semaines,SemainesAdmin)
admin.site.register(CreneauxColleurs,CreneauxColleursAdmin)
admin.site.register(GroupeColles,GroupeCollesAdmin)
admin.site.register(Colloscope,ColloscopeAdmin)
admin.site.register(Renseignements,RenseignementsAdmin)

