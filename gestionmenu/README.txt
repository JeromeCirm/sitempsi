

Gestion de site : a besoin de la partie "base"
  
  à mettre dans urls.py du projet général avant 'base.urls':
           path('', include('gestionmenu.urls')),

 penser à modifier donnees_perso et donnees_classe
 
la partie generic.py contient l'essentiel pour une base de site
la partie classe.py   contient ce qui est spécifique à une classe/la classe MPSI
la partie special_jerome.py contient les fonctions d'initialisation pour la classe

dans  generic.autorise_menu(...) : 
   gestion_menu est à part : n'est mise dans le menu que si l'utilisateur est un gestionnaire

dans view.download : 
  mettre à jour les droits de lecture pour le type 'parcoursup' si besoin en choisissant
  le bon menu à la palce de 'lire les fiches de renseignements'
   
