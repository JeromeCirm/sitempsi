
from django.urls import path,include,re_path
from . import views

urlpatterns = [
    path('menu/<int:numero>',views.menu,name='menu'),
    path('ajout_fichier/<int:pk>',views.ajout_fichier,name='ajout_fichier'),
    path('supprime_fichier/<int:pk>',views.supprime_fichier,name='supprime_fichier'),
    path('modifie_fichier/<int:pk>',views.modifie_fichier,name='modifie_fichier'),
    path('modifie_ordre_fichier/<int:pk>/<str:up>',views.modifie_ordre_fichier,name='modifie_ordre_fichier'),
    path('ajout_menu/<int:pk>',views.ajout_menu,name='ajout_menu'),
    path('supprime_menu/<int:pk>',views.supprime_menu,name='supprime_menu'),
    path('modifie_menu/<int:pk>',views.modifie_menu,name='modifie_menu'),
    path('modifie_ordre_menu/<int:pk>/<str:up>',views.modifie_ordre_menu,name='modifie_ordre_menu'),
    path('modifie_fichier_unique/<int:pk>',views.modifie_fichier_unique,name='modifie_fichier_unique'),
    path('download/<int:pk>',views.download,{'letype':'file'},name='download'),
    path('recupere_eleves',views.recupere_eleves,name='recupere_eleves'),
    ]