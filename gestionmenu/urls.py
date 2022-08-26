
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
    path('download/prog<int:pk>',views.download,{'letype':'prog'},name='download'),
    path('download/exos<int:pk>',views.download,{'letype':'exos'},name='download'),    path('recupere_eleves',views.recupere_eleves,name='recupere_eleves'),
    path('ajout_prog_colle_math',views.ajout_prog_colle_math,name='ajout_prog_colle_math'),
    path('supprime_prog_colle_math/<int:pk>',views.supprime_prog_colle_math,name='supprime_prog_colle_math'),
    path('modifie_prog_colle_math/<int:pk>',views.modifie_prog_colle_math,name='modifie_prog_colle_math'),
    ]