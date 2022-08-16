
Base de site contenant la gestion du login

penser à modifier config_mail_perso et settings_mail
penser à modifier  la fonction "home" dans "views" 
   afin d'adapter la page par défaut en mettant la ligne suivante
   dans urls.py du projet général :
          path('', include('base.urls')),

