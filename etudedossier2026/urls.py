from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
     path('affichage', views.affichage,name='affichage_etudedossier2026'),
     path('traitement', views.traitement,name='traitement_etudedossier2026'),
     path('gestion', views.gestion,name='gestion_etudedossier2026'),
     path('download/<str:nom>',views.download,name='download_etudedossier2026'),
     path('', views.selection,name='selection_etudedossier2026')
]