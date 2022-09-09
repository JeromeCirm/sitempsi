
# fonctions du menu de gestion 
from sqlalchemy import create_engine
import pandas as pd
from django.contrib.auth.models import User
from .donnees_classe import *
from .generic import *
from .models import *

# on garde login déjà existants et profs,en vérifiant que ce ne sont pas des élèves
# suppression des "vieux" login profs
def maj_comptes_profs(context):
    a_effacer=User.objects.filter(groups=groupe_profs).exclude(username__in=liste_profs)
    a_effacer.delete()
    context["msg"]=""
    for unprof in liste_profs:
        try:
            user=User.objects.get(username=unprof)
            if groupe_profs in user.groups.all():
                context["msg"]+=unprof+" existe déjà en prof,"
            else:
                context["msg"]+=unprof+" existe déjà et n'est pas prof : on arrête."
                return
        except:
            if creation_compte(unprof,mdp_profs,[groupe_profs])==None:
                context["msg"]="erreur lors de la création du compte de "+unprof
                return              
            context["msg"]+=unprof+" est créé,"

def maj_comptes_colleurs(context):
    lesgroupes=[(groupe_colleurs_math,liste_colleurs_math),(groupe_colleurs_anglais,liste_colleurs_anglais),
    (groupe_colleurs_philo,liste_colleurs_philo),(groupe_colleurs_physique,liste_colleurs_physique)]
    context["msg"]=""
    for groupe,liste in lesgroupes:
        a_effacer=User.objects.filter(groups=groupe).exclude(username__in=liste_profs).exclude(username__in=liste)
        a_effacer.delete()
        for uncolleur in liste:
            try:
                user=User.objects.get(username=uncolleur)
                if groupe in user.groups.all():
                    context["msg"]+=uncolleur+" existe déjà en colleur,"
                elif groupe_profs in user.groups.all():
                    user.groups.add(groupe)
                    context["msg"]+=uncolleur+" existait en prof - ajout en colleur,"
                else:
                    context["msg"]+=uncolleur+" existe déjà et n'est pas prof ou colleur : on arrête."
                    return
            except:
                if creation_compte(uncolleur,mdp_colleurs,[groupe])==None:
                    context["msg"]="erreur lors de la création du compte de "+uncolleur
                    return                
                context["msg"]+=uncolleur+" est créé,"

def reinitialisation_eleves(context):
    anciens=User.objects.filter(groups=groupe_eleves)
    anciens.delete()          # on efface tous les anciens élèves.
    doublons=User.objects.filter(username__in=liste_eleves)
    if len(doublons)!=0:
        context["msg"]="un login élève est déjà utilisé :"    # liste à vérifier, il y a déjà un utilisateur avec ce nom
        for x in doublons:
            context["msg"]+=" "+x.username+","
        return
    for uneleve in liste_eleves:
        if creation_compte(uneleve,mdp_eleves,[groupe_eleves])==None:
            context["msg"]="erreur lors de la création du compte de "+uneleve
            return
        renseignements=Renseignements.objects.create(login=uneleve,année=annee_courante)
        renseignements.save()
    context["msg"]="reinitialisation des logins eleves terminée"

def creation_groupes_colles_s1(context):
    GroupeColles.objects.all().delete()
    numero=1
    for ungroupe in perso_groupes_colles_s1:
        groupe=GroupeColles(numero=numero)
        groupe.save()
        for uneleve in ungroupe:
            try:
                groupe.eleves.add(User.objects.get(username=uneleve))
            except:
                context["msg"]="erreur en ajoutant "+uneleve+" au groupe "+str(numero)
                return
        numero+=1
    context["msg"]="groupes de colles créés pour le semestre 1"

def creation_groupes_colles_s2(context):
    GroupeColles.objects.filter(numero__gte=17).delete()
    numero=17
    for ungroupe in perso_groupes_colles_s2:
        groupe=GroupeColles(numero=numero)
        groupe.save()
        for uneleve in ungroupe:
            try:
                groupe.eleves.add(User.objects.get(username=uneleve))
            except:
                context["msg"]="erreur en ajoutant "+uneleve+" au groupe "+str(numero)
                return
        numero+=1
    context["msg"]="groupes de colles créés pour le semestre 2"

def creation_creneaux_colles(context):
    CreneauxColleurs.objects.all().delete()
    liste=[(creneaux_math,"math"),(creneaux_physique,"physique"),(creneaux_anglais,"anglais")]
    for liste_creneaux,matiere in liste:
        for numero,creneau in enumerate(liste_creneaux,start=1):
            try:
                CreneauxColleurs(colleur=User.objects.get(username=creneau[0]),jour=creneau[1],
                horaire=creneau[2],salle=creneau[3],numero=numero,matière=matiere).save()
            except:
                context["msg"]="erreur lors de la création du créneau "+str(creneau)
                return
    context["msg"]="créneaux de colles créés"

def creation_colloscope(context):
    # à revoir avec la nouvelle gestion des créneaux
    # physique/anglais sont séparés dans la base de données maintenant
    # et non à la suite mélangés
    Colloscope.objects.all().delete()
    lessemaines=Semaines.objects.all()
    for lasemaine in lessemaines:
        semaine=lasemaine.numero
        for groupe in range(1,17):
            legroupe=GroupeColles.objects.get(numero=groupe)
            valeurmath=(semaine+groupe-2)%16+1
            valeurautre=valeurmath

            collemath=CreneauxColleurs.objects.get(numero=valeurmath,matière="math")
            item=Colloscope(creneau=collemath,groupe=legroupe,semaine=lasemaine)
            item.save()
            if valeurautre%2==1: # colle de physique
                autrecolle=CreneauxColleurs.objects.get(numero=(valeurautre+1)//2,matière="physique")
            else:
                if groupe==1:
                    valeurautre=18  # le groupe 1 a allemand et non anglais
                if groupe%2==1 and valeurautre==10:
                    valeurautre=(semaine-1)%16+1 # prend la place du groupe 1
                autrecolle=CreneauxColleurs.objects.get(numero=valeurautre//2,matière="anglais")
            item=Colloscope(creneau=autrecolle,groupe=legroupe,semaine=lasemaine)
            item.save()
    context["msg"]="colloscope créé"

def export_renseignements(context):
    def clean(str):
        try:
            return str.replace('\\r\\n','\r\n').replace('\\','')
        except:
            return ""
    def clean_int(str):
        try:
            return int(str)
        except:
            return 0
    def clean_bool(str):
        if str=="True" or str=="true":
            return True
        if str=="False" or str=="false":
            return False
        return None
    df=pd.read_excel('export_renseignements.xls')
    Renseignements.objects.filter(année=2021).delete()
    for index, row in df.iterrows():
        obj=Renseignements.objects.create(login=clean(row["nomusage"]))
        obj.année=2021
        obj.nomusage=clean(row["nomusage"])
        obj.prenomusage=clean(row["prenomusage"])
        if row["nomusage"]=='GUERARD':
            obj.save()
            continue
        elif row["nomusage"]=='Ceban':
            obj.naissance='2003-12-22'
        else:
            obj.naissance=row["naissance"]
        obj.tempstrajet=clean_int(row["tempstrajet"])
        obj.seullogement=clean_bool(row["seullogement"])
        obj.motivationprepa=clean(row["motivationprepa"])
        obj.lyceeorigine=clean(row["lyceeorigine"])
        obj.villelyceeorigine=clean(row["villelyceeorigine"])
        obj.professionparents=clean(row["professionparents"])
        obj.freressoeurs=clean(row["freressoeurs"])
        obj.calculatrice=clean(row["calculatrice"])
        obj.accessordinateur=clean_bool(row["accessordinateur"])
        obj.connexioninternet=clean_bool(row["connexioninternet"])
        obj.coursconfinementmath=row["coursconfinementmath"]
        obj.coursconfinementphysique=row["coursconfinementphysique"]
        obj.confinementcommentaire=clean(row["confinementcommentaire"])
        obj.notesbac=clean(row["notesbac"])
        obj.choix1=row["choix1"]
        obj.choix2=row["choix2"]
        obj.choix3=row["choix3"]
        obj.choix4=row["choix4"]
        obj.option=row["option"]
        obj.pdf.set([])
        obj.save()
