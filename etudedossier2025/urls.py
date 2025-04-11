from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
     path('affichage', views.affichage,name='affichage_etudedossier2025'),
     path('traitement', views.traitement,name='traitement_etudedossier2025'),
     path('gestion', views.gestion,name='gestion_etudedossier2025'),
     path('download/<str:nom>',views.download,name='download_etudedossier2025'),
     path('', views.selection,name='selection_etudedossier2025')
]