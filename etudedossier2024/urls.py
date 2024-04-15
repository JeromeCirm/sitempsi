from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
     path('affichage', views.affichage,name='affichage_etudedossier2024'),
     path('traitement', views.traitement,name='traitement_etudedossier2024'),
     path('gestion', views.gestion,name='gestion_etudedossier2024'),
     path('download/<str:nom>',views.download,name='download_etudedossier2024'),
     path('', views.selection,name='selection_etudedossier2024')
]