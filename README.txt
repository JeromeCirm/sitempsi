 Pour installer correctement : 
 -créer (ou copier) une version de db.sqlite3
 -créer un fichier sitempsi/config.py, contenant les données sensibles de la configuration



 A finaliser :
  -enlever nomusage/prénomusage dans renseignement : inutile maintenant : c'est user.firstname/lastname
       vérifier que c'est utilisé nulle part
        afficher justement firstname/lastname à la place

    enlever dans forms.py



nouvelle année : 

-creation du répertoire, a faire avec environnement dans la racine :
   python manage.py startapp etudedossier2024
-copier une ancienne version à la place
     -effacer le contenu de migrations, transfert_fiche, stockage, fiches
     -renommer les 2024 en ***  :  static/etudedossier2024, template/etudedossier2024, basedossier2024.html
     - modifier le début {% extends 'basedossier2024.html' %} des fichiers html
     - modifier l'url {% url 'selection_etudedossier2024' %} dans les mêmes fichiers : 
           affichage (2 modifs), basedossier ( 2 modifs), gestion(3 modifs), selection (4 modifs), traitement(4 modifs)
     - pareil dans les fichiers .py qui suivent (utiliser replace)
-modifier le .gitignore  (fiches, stockage, transfert_fiche)
-partie principale du site : 
    - sitempsi.settings.py :
         -installer l'app :     'etudedossier2024.apps.Etudedossier2024Config', 
         -modifier le répertoire des templates :  BASE_DIR/'etudedossier2024/templates/etudedossier2024'
    - sitempsi.urls.py : 
             path('etudedossier2024/', include('etudedossier2024.urls')),
    - gestionmenu.view.py : 
         - au début : "from etudedossier2024.views import selection as selection2024"
         - puis dans list_menu, ajouter "parcoursup2024"
         - puis juste après, créer une fonction "parcoursup2024"
-optionnel : gestion des lycées : 
    - partie aa_doc annexes à modifier/lancer (quelques warning : vérifier un jour)
    - modifier traitement.html pour faire apparaitre la nouvelle année
    

création du répertoire fiche si c'est après un git pull
makemigrations/migrate

en mode admin, créer un menu avec en lien "parcoursup2024"

Télécharger les fiches, le reste se fait en gestion sur le site
