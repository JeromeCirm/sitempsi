#
#  Penser à créer les semaines de colles à la main
#  groupe de colles  1-16 pour s1  et 17-32 pour s2 (15,16 supprimés si besoin, s2 commence toujours à 17)
from .donnees_perso import *

JOLI_NOM=MY_JOLI_NOM # on utilise login ou prénom/nom?

liste_eleves=perso_liste_eleves # login des élèves
prof_avec_colles =perso_prof_avec_colles # dictionnaire {"prof" : "nom_groupe_colleur"}
# pour les matières avec colle
liste_profs=perso_liste_autres_profs+list(prof_avec_colles.keys()) # login des profs
liste_colleurs_math=perso_liste_colleurs_math # login des colleurs de math
liste_colleurs_physique=perso_liste_colleurs_physique # login des colleurs de physique
liste_colleurs_anglais=perso_liste_colleurs_anglais # login des colleurs d'anglais
liste_colleurs_philo=perso_liste_colleurs_philo # login des colleurs de philo
dic_pronote=perso_dic_pronote  # dictionnaire  {login : "nom;prénom"} pour créer les fichiers PRONOTE

# mot de passe à la création du compte
mdp_eleves =perso_mdp_eleves     
mdp_profs = perso_mdp_profs
mdp_colleurs = perso_mdp_colleurs

#pour le colloscope
groupes_colles_s1=perso_groupes_colles_s1 # liste de listes de login
groupes_colles_s2=perso_groupes_colles_s2 # liste de listes de login
creneaux_math =perso_creneaux_math  # liste de créneaux  ["username","jour","heure","salle"]
creneaux_physique=perso_creneaux_physique
creneaux_anglais=perso_creneaux_anglais

annee_courante=2022  # année du mois de septembre en cours
affiche_choix_option = False  # choix d'option fin du premier semestre
affiche_choix_orientation = False  # choix d'orientation de fin d'année