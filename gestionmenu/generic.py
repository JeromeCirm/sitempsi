# gestion de menu : 
# fonctions liées à la version basique utilisable par chaque utilisateur
# et la page par défaut
# pour la page par défaut, les fichiers sont sauvegardés dans
# le répertoire private_files/fichiers/ (changeable dans models.py)
from django.contrib.auth import authenticate,login
from django.shortcuts import render,redirect
from .models import Menu,Fichier
from base.models import Utilisateur
from django.contrib.auth.models import User,Group
from django.db.models import Case,When
from .donnees_classe import *
import datetime

liste_generic = ['liste_fichiers','parametres_compte','gestion_menu']

try:
    groupe_eleves=Group.objects.get(name='eleves')
    groupe_profs=Group.objects.get(name='profs')
    groupe_colleurs_math=Group.objects.get(name='colleurs_math')
    groupe_colleurs_physique=Group.objects.get(name='colleurs_physique')
    groupe_colleurs_anglais=Group.objects.get(name='colleurs_anglais')
    groupe_colleurs_philo=Group.objects.get(name='colleurs_philo')
except:
    print('attention il faut créer les groupes utilisateurs indiqués dans generic.py !')

def joli_nom(user):  # renvoie le login ou   prénom+nom si cela a été renseigné
    if JOLI_NOM and user.first_name!="" and user.last_name!="":
        return user.first_name+" "+user.last_name
    return user.username

def date_fr(date,annee=False):
    # transforme la date en francais, avec ou sans l'année
    if annee: 
        return date.strftime("%d/%m/%y")
    else:
        return date.strftime("%d/%m")

# échange deux éléments d'un requete liste selon le champ ordre
def echange(liste,ordre1,ordre2): 
    liste.filter(ordre__in=[ordre1,ordre2]).update(ordre=Case(When(ordre=ordre1,then=ordre2),When(ordre=ordre2,then=ordre1)) )

def est_gestionnaire_menu(user,menu):
    # teste si l'utilisateur est gestionnaire du menu
    for x in menu.gestionnaires.all():
        if x==user:
            return True
    return False

def autorise_menu(user,menu):
    # teste si on autorise ce menu pour l'utilisateur 
    if menu.nom=="gestion_menu":
        menus_en_gestion=Menu.objects.filter(gestionnaires=user)
        return len(menus_en_gestion)>0
    lesgroupes=user.groups.all()
    if user.is_superuser:
        return True
    for x in menu.groupes.all():
        if x in lesgroupes:
            return True
    return est_gestionnaire_menu(user,menu)

def menu_navigation(request):
    # liste des menus accessibles à l'utilisateur connecté
    liste=Menu.objects.all().order_by('ordre')
    tableau=[]
    for item in liste : 
        if item.parent==0 and autorise_menu(request.user,item):
            subtableau=[]
            for subitem in liste : 
                if subitem.parent==item.id and autorise_menu(request.user,subitem):
                    if subitem.fonction[0:4]=="lien":
                        subtableau.append((subitem.nom,subitem.id,subitem.fonction[4:],True))
                    else:
                        subtableau.append((subitem.nom,subitem.id,subitem.fonction,False))
            tableau.append((item.nom,item.id,item.fonction,subtableau))
    return tableau

def liste_fichiers(request,numero,context):
    item=Menu.objects.get(id=numero)
    if item.parent!=0:
        parent=Menu.objects.get(id=item.parent)
        item.nom=parent.nom+' : '+item.nom
    context['lemenu']=item
    # on récupère la liste des fichiers de la page
    gestionnaire=est_gestionnaire_menu(request.user,item)
    if gestionnaire:
        context['fichier']=Fichier.objects.filter(menu=numero)
    else:
        context['fichier']=Fichier.objects.filter(menu=numero).exclude(date_parution__gt=datetime.datetime.now())
    # on détermine si l'utilisateur est un gestionnaire de cette page
    context['gestionnaire']=gestionnaire
    return render(request,'gestionmenu/listefichiers.html',context)

def creation_compte(login,password,liste_groupe=[]):
    try:
        user=User.objects.create_user(username=login,password=password)
        user.save()
        utilisateur=Utilisateur.objects.create(user=user,en_attente_confirmation=False)
        utilisateur.save()
        for group in liste_groupe:
            user.groups.add(group)
        return user
    except:
        return None

def parametres_compte(request,numero,context):
    try:
        context['changepassword']=False
        context['changepasswordreussi']=False
        if (not (request.user.is_superuser) ) and request.method=="POST" and "password" in request.POST:
                context['changepassword']=True
                old=request.POST.get('password')
                new=request.POST.get('newpassword')
                newconfirm=request.POST.get('newpasswordconfirm')
                user=authenticate(request,username=request.user.username,password=old)
                if (new==newconfirm) and (user is not None):
                    context['changepasswordreussi']=True
                    user=User.objects.get(username=request.user.username)
                    user.set_password(new)
                    user.save()
                    login(request,user)
        if (not (request.user.is_superuser) ) and request.method=="POST" and "mail" in request.POST:
            request.user.email=request.POST["mail"]
            if not(JOLI_NOM):
                request.user.first_name=request.POST["prenomusage"]
                request.user.last_name=request.POST["nomusage"]
            request.user.save()
            context["msg"]="paramètres mis à jour"
        context["mail"]=request.user.email
        context["prenomusage"]=request.user.first_name
        context["nomusage"]=request.user.last_name
        context["jolinom"]=JOLI_NOM
        return render(request,'gestionmenu/parametres_compte.html',context)
    except:
        return redirect('/home')

def gestion_menu(request,numero,context):
    lesmenus=Menu.objects.filter(gestionnaires=request.user,parent=0)
    menus=[]
    for unmenu in lesmenus:
        lessousmenu=Menu.objects.filter(parent=unmenu.id)
        menus.append({"lemenu":unmenu,"lessousmenus":lessousmenu})
    context['menus']=menus
    lesmenus_unique=Menu.objects.filter(gestionnaires=request.user,fonction='fichier_unique')
    for unmenu in lesmenus_unique:
        if unmenu.parent!=0:
            parent=Menu.objects.get(pk=unmenu.parent)
            unmenu.nom=parent.nom+": "+unmenu.nom
            try:
                fichier=Fichier.objects.get(menu=unmenu)
                unmenu.nomfichier="fichier : "+fichier.nomfichier
            except:
                unmenu.nomfichier="pas de fichier "
    context['menus_unique']=lesmenus_unique
    return render(request,'gestionmenu/gestion_menu.html',context)

def est_colleur(user):
    # user est-il un colleur?
    for nom_groupe in prof_avec_colles.values():
        groupe=Group.objects.get(name=nom_groupe)
        if groupe in user.groups.all():
            return True
    return False

def est_gestionnaire_colle(user,colleur_name):
    # colleur_name es-il un colleur pour user?
    for prof,nom_groupe in prof_avec_colles.items():
        if user.username==prof:
            groupe=Group.objects.get(name=nom_groupe)
            colleur=User.objects.get(username=colleur_name)
            if groupe in colleur.groups.all():
                return True
    return False
 