from django.shortcuts import render,redirect
from sqlalchemy import null
from base.fonctions import auth
from .models import Menu
from .forms import *
from django.db.models import Max
from wsgiref.util import FileWrapper
from django.http.response import HttpResponse
from django.http import FileResponse
import json
from .generic import *
from .classe import *
import locale
locale.setlocale(locale.LC_ALL,'fr_FR.UTF-8')
import sys
sys.path.append("..")
from config_generale import *
from etudedossier2022.views import selection as selection2022
from etudedossier2023.views import selection as selection2023

# liste des fonctions correspondant à un menu perso
# à cela, on ajouter la fonction "liste_fichier" 
# qui correspond à un menu générique créé par un gestionnaire de menu
liste_menu=liste_generic + liste_classe+['fichier_unique','parcoursup2022','parcoursup2023']

try:
    from .hors_git.fonctions_hors_git import * 
    liste_menu+=liste_hors_git
except:
    print("pas d'hors-git trouvé")
    pass

def parcoursup2022(request,numero,context):
    return selection2022(request)

def parcoursup2023(request,numero,context):
    return selection2023(request)

@auth(None)
def menu(request,numero):
    context={"menu":menu_navigation(request)}
    context["titresite"]=TITRE_SITE
    if True: #try:
        lemenu=Menu.objects.get(pk=numero)
        if autorise_menu(request.user,lemenu):
            nom_fonction=str(lemenu.fonction)
            if nom_fonction in liste_menu:
                return globals()[str(nom_fonction)](request,numero,context)
        return redirect('/home')
    #except:
        print('erreur dans la fonction : enlever try except de la fonction menu de views.py')
        return redirect('/home')

@auth(None)
def home(request):
    context={"menu":menu_navigation(request)}
    context["titresite"]=TITRE_SITE
    lesgroupes=request.user.groups.all()
    if groupe_eleves in lesgroupes:
        context["eleve"]=True
        lessemaines=Semaines.objects.all().order_by("numero")
        context["lessemaines"]=[{"numero":x.numero,"date":date_fr(x.date,True)} for x in lessemaines]
        try:
            context["annonce"]=Divers.objects.get(label="annonce").contenu
        except:
            context["annonce"]=""
    if groupe_profs in lesgroupes:
        if request.method=='POST':
            try:
                annonce=Divers.objects.get(label='annonce')
                annonce.contenu=request.POST.get('annonce')
                annonce.save()  
            except:
                try:
                    annonce=Divers.objects.create(label='annonce',contenu=request.POST.get('annonce'))
                    annonce.save() 
                except:
                    pass
        context["prof"]=True
        try:
            context["annonce"]=Divers.objects.get(label="annonce").contenu
        except:
            context["annonce"]=""
    return render(request,'gestionmenu/home.html',context)

def fichier_unique(request,numero,context):
    item=Menu.objects.get(id=numero)
    if item.parent!=0:
        parent=Menu.objects.get(id=item.parent)
        item.nom=parent.nom+' : '+item.nom
    context['lemenu']=item
    # on récupère le fichier de la page
    try:
        lefichier=Fichier.objects.get(menu=numero)
        return download(request,"file",lefichier.pk)
    except:
        return render(request,'gestionmenu/fichier_unique.html',context)

def ajout_fichier(request,pk):
    try:
        menu=Menu.objects.get(id=pk)
        if menu.fonction!="liste_fichiers" or not est_gestionnaire_menu(request.user,menu):
            return redirect('/home')
    except:
        return redirect('/home')
    form=FichierForm()
    if request.method=="POST":
        obj=Fichier.objects.create(description="bidon",ordre=0,menu=menu)
        form=FichierForm(request.POST,request.FILES,instance=obj)
        if form.is_valid():
            new_fichier=form.save(commit=False)
            try:
                res=Fichier.objects.all().aggregate(Max('ordre'))
                new_fichier.ordre=res['ordre__max']+1
            except :
                new_fichier.ordre=1
            if 'fichier' in request.FILES:
                new_fichier.nomfichier=request.FILES['fichier']
            new_fichier.date_parution=request.POST["date_parution"]
            try:
                new_fichier.save()
            except:
                new_fichier.date_parution=datetime.datetime.now()
                new_fichier.save()
            return redirect('/menu/'+str(pk))
    context={"menu":menu_navigation(request)}
    context["titresite"]=TITRE_SITE
    context['form']=form
    context['idmenu']=pk
    return render(request,'gestionmenu/ajout_fichier.html',context)

def modifie_fichier(request,pk):
    try:
        obj=Fichier.objects.get(id=pk)
        menu=obj.menu
        if menu.fonction!="liste_fichiers" or not est_gestionnaire_menu(request.user,menu):
            return redirect('/home')
        if request.method=="POST":
                if 'description' in request.POST:
                    form=FichierForm(request.POST,instance=obj)
                    if form.is_valid():
                        form.save()
                        obj.date_parution=request.POST["date_parution"]
                        try:
                            obj.save()
                        except:
                            obj.date_parution=datetime.datetime.now()
                            obj.save()
                if 'fichier-clear' in request.POST:
                    obj.fichier.delete()
                elif 'fichier' in request.FILES:
                    form=FichierForm({'description':obj.description},request.FILES,instance=obj)
                    if obj.fichier!=None:
                        obj.fichier.delete()
                    if form.is_valid():
                        new_record=form.save(commit=False)
                        new_record.nomfichier=request.FILES['fichier']
                        new_record.save()  
                return redirect('/menu/'+str(menu.id))
        context={"menu":menu_navigation(request)}
        context["titresite"]=TITRE_SITE
        context['nom_fichier']=obj.nomfichier
        formdescription=FichierFormDescription(instance=obj)
        formfichier=FichierFormFichier(instance=obj)
        context['formdescription']=formdescription
        context['formfichier']=formfichier
        context["date_parution"]=str(obj.date_parution)
        return render(request,'gestionmenu/modifie_fichier.html',context)
    except:
        return redirect('/home')

# le fichier apparaissant en premier est celui d'ordre le plus élevé
def modifie_ordre_fichier(request,pk,up="True"):
    try:
        obj=Fichier.objects.get(id=pk)
        menu=obj.menu
        if menu.fonction!="liste_fichiers" or not est_gestionnaire_menu(request.user,menu):
            return redirect('/home')
        liste=Fichier.objects.filter(menu=menu).order_by('-ordre')
        i=0
        while i<len(liste) and liste[i].id!=int(pk):
           i+=1  
        if i>0 and up=="True":
            echange(liste,liste[i].ordre,liste[i-1].ordre) 
        if i<len(liste)-1 and up=="False": 
            echange(liste,liste[i].ordre,liste[i+1].ordre) 
        return redirect('/menu/'+str(menu.id))
    except:
        return redirect('/home')

def supprime_fichier(request,pk):
    try:
        obj=Fichier.objects.get(id=pk)
        menu=obj.menu
        if not est_gestionnaire_menu(request.user,menu):
            return redirect('/home')
    except:
        return redirect('/home')
    if request.method=="POST" and "validation" in request.POST:
            obj.delete()
            return redirect('/menu/'+str(menu.id))
    context={"menu":menu_navigation(request)}
    context["titresite"]=TITRE_SITE
    context['obj']="le fichier "+str(obj.nomfichier)
    return render(request,'gestionmenu/delete.html',context)

def ajout_menu(request,pk):
    try:
        menu=Menu.objects.get(id=pk)
        if not est_gestionnaire_menu(request.user,menu):
            return redirect('/home')
        form=MenuForm()
        if request.method=="POST":
            form=MenuForm(request.POST)
            if form.is_valid:
                new_menu=form.save(commit=False)
                new_menu.parent=pk
                request.POST['type_de_menu']
                if request.POST['type_de_menu']=="l":
                    new_menu.fonction="liste_fichiers"
                else:
                    new_menu.fonction="fichier_unique"
                try:
                    res=Menu.objects.filter(parent=pk).aggregate(Max('ordre'))
                    new_menu.ordre=res['ordre__max']+1
                except :
                    new_menu.ordre=1
                new_menu.save()
                for ungroupe in menu.groupes.all():
                    new_menu.groupes.add(ungroupe)
                for user in menu.gestionnaires.all():
                    new_menu.gestionnaires.add(user)
                context={"menu":menu_navigation(request)}
                return gestion_menu(request,0,context)
        context={"menu":menu_navigation(request)}
        context["titresite"]=TITRE_SITE
        context['form']=form
        context['idmenu']=menu.nom
        return render(request,'gestionmenu/ajout_menu.html',context)
    except:
        return redirect('/home')

def modifie_menu(request,pk):
    try:
        menu=Menu.objects.get(id=pk)
        parent=Menu.objects.get(id=menu.parent)
        if not est_gestionnaire_menu(request.user,parent):
            return redirect('/home')
        if request.method=="POST":
            form=MenuFormSimple(request.POST,instance=menu)
            if form.is_valid():
                form.save()
                context={"menu":menu_navigation(request)}
                return gestion_menu(request,0,context)               
        context={"menu":menu_navigation(request)}
        context["titresite"]=TITRE_SITE
        context['idmenu']=parent.nom
        form=MenuFormSimple(instance=menu)
        context['form']=form
        return render(request,'gestionmenu/ajout_menu.html',context)
    except:
        return redirect('/home')

def modifie_ordre_menu(request,pk,up="True"):
    try:
        menu=Menu.objects.get(id=pk)
        parent=Menu.objects.get(id=menu.parent)
        if not est_gestionnaire_menu(request.user,parent):
            return redirect('/home')
        listemenus=Menu.objects.filter(parent=menu.parent).order_by('ordre')
        i=0
        while i<len(listemenus) and listemenus[i].id!=int(pk):
           i+=1  
        if i>0 and up=="True":
            echange(listemenus,listemenus[i].ordre,listemenus[i-1].ordre) 
        if i<len(listemenus)-1 and up=="False": 
            echange(listemenus,listemenus[i].ordre,listemenus[i+1].ordre) 
        context={"menu":menu_navigation(request)}
        context["titresite"]=TITRE_SITE
        return gestion_menu(request,0,context)
    except:
        return redirect('/home')

def supprime_menu(request,pk):
    try:
        menu=Menu.objects.get(id=pk)
        parent=Menu.objects.get(id=menu.parent)
        if not est_gestionnaire_menu(request.user,parent):
            return redirect('/home')
        if request.method=="POST" and "validation" in request.POST:
            if menu.fonction=="liste_fichiers" or menu.fonction=="fichier_unique":
                menu.delete()
                context={"menu":menu_navigation(request)}
            else:
                context={"menu":menu_navigation(request)}
                context["msg"]="impossible de supprimer ce menu"
            return gestion_menu(request,0,context)
        context={"menu":menu_navigation(request)}
        context["titresite"]=TITRE_SITE
        context['obj']="le sous-menu '"+str(menu.nom)+"' de "+str(parent.nom)
        return render(request,'gestionmenu/delete.html',context)
    except:
        return redirect('/home')

def modifie_fichier_unique(request,pk):
    try:
        context={"menu":menu_navigation(request)}
        context["titresite"]=TITRE_SITE
        menu=Menu.objects.get(id=pk)
        if not (est_gestionnaire_menu(request.user,menu) and menu.fonction=="fichier_unique"):
            return redirect('/home')
        if request.method=="POST":
            if 'fichier-clear' in request.POST:
                Fichier.objects.filter(menu=menu).delete()                
                return gestion_menu(request,0,context)
            elif 'fichier' in request.FILES:
                Fichier.objects.filter(menu=menu).delete()
                obj=Fichier.objects.create(description="",ordre=0,menu=menu)
                form=FichierForm({'description':""},request.FILES,instance=obj)
                if form.is_valid():
                    new_record=form.save(commit=False)
                    new_record.nomfichier=request.FILES['fichier']
                    new_record.save()
            return gestion_menu(request,0,context)            
        else:
            try:
                obj=Fichier.objects.get(menu=menu)              
                form=FichierUniqueForm(instance=obj)
            except:
                form=FichierUniqueForm()
            context['form']=form
            context['nommenu']=menu.nom
            return render(request,'gestionmenu/modifie_fichier_unique.html',context)
    except:
        return redirect('/home')

def recupere_eleves(request):
    try:
        r=Renseignements.objects.filter(année=request.POST["annee"])
        response_data = {"eleves":[str(x.login) for x in r]}
    except:
        response_data = {"eleves":[]}
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def auth_prog_colle_math(request):
    try:
        menu=Menu.objects.get(fonction="programme_colle_math")
        return est_gestionnaire_menu(request.user,menu)
    except:
        return False

def ajout_prog_colle_math(request):
    if auth_prog_colle_math(request):
        context={"menu":menu_navigation(request)}
        context["titresite"]=TITRE_SITE
        form=ProgColleMathForm()
        context['form']=form
        if request.method=="POST":
            obj=ProgColleMath.objects.create(description="bidon",numero=0)
            form=ProgColleMathForm(request.POST,request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                return redirect('/menu/'+str(Menu.objects.get(fonction="programme_colle_math").id))
        return render(request,'gestionmenu/ajout_prog_colle_math.html',context)
    return redirect('/home')

def supprime_prog_colle_math(request,pk):
    if auth_prog_colle_math(request):
        context={"menu":menu_navigation(request)}
        context["titresite"]=TITRE_SITE
        if request.method=="POST":
            obj=ProgColleMath.objects.get(id=pk)
            obj.delete()
            return redirect('/menu/'+str(Menu.objects.get(fonction="programme_colle_math").id))
        context['obj']="programme de colle n° "+str(pk)
        return render(request,'gestionmenu/delete.html',context)
    return redirect('/home')

def modifie_prog_colle_math(request,pk):
    # attention : fichiers non supprimés lors de la suppression d'un 
    # programme de colle
    if auth_prog_colle_math(request):
        context={"menu":menu_navigation(request)}
        context["titresite"]=TITRE_SITE
        obj=ProgColleMath.objects.get(id=pk)
        if request.method=="POST":
            if 'description' in request.POST:
                form=ProgColleMathForm(request.POST,instance=obj)
                if form.is_valid():
                    form.save()
            if 'programme' in request.FILES:
                form=ProgColleMathForm({'description':obj.description,'numero':obj.numero},request.FILES,instance=obj)
                if obj.programme!=None:
                    obj.programme.delete()
                if form.is_valid():
                    form.save()  
            if 'exercices' in request.FILES:
                form=ProgColleMathForm({'description':obj.description,'numero':obj.numero},request.FILES,instance=obj)
                if obj.exercices!=None:
                    obj.exercices.delete()
                if form.is_valid():
                    form.save()  
            return redirect('/menu/'+str(Menu.objects.get(fonction="programme_colle_math").id))
        context['id']=obj.id
        formdescription=ProgColleMathFormDescription(instance=obj)
        formprogramme=ProgColleMathFormProgramme(instance=obj)
        formexercices=ProgColleMathFormExercices(instance=obj)
        context['formprogdescription']=formdescription
        context['formprogprogramme']=formprogramme
        context['formprogexercices']=formexercices
        return render(request,'gestionmenu/modifie_prog_math.html',context)
    else :
        return redirect('/home')

def maj_notes_colles(request):
    response_data = {"resultat" : "erreur"}
    try:
        if request.POST["colleur"]=="":
            # un colleur modifie une de ses notes
            colleur=request.user
        else:
            # un gestionnaire modifie une note
            colleur_name=request.POST["colleur"]
            if est_gestionnaire_colle(request.user,colleur_name):
                colleur=User.objects.get(username=colleur_name)
            else:
                return redirect('\home')
        # phase de modification de la note
        eleve=User.objects.get(username=request.POST["eleve"])
        semaine=Semaines.objects.get(numero=request.POST["semaine"])
        note=request.POST["note"]
        try:
            # la note existe déjà
            notecolle=NotesColles.objects.get(colleur=colleur,eleve=eleve,semaine=semaine)
            if note=="":
                notecolle.delete()
            else:
                notecolle.note=note
                notecolle.save()
        except:
            # la note n'existe pas
            if note!="": # else impossible normalement
                notecolle=NotesColles(colleur=colleur,eleve=eleve,semaine=semaine,note=note)
                notecolle.save()
    except:
        print("erreur")
    return HttpResponse(json.dumps(response_data), content_type="application/json")    


def recuperation_notes_colles(request):
    # attention : droits à gérer
    response_data = {}
    try:
        if request.method=="POST" and "semaine" in request.POST and "colleur" in request.POST:
            semaine=Semaines.objects.get(numero=int(request.POST["semaine"]))
            if request.POST["colleur"]=="all":
                # un gestionnaire récupère toutes les colles
                # de la semaine
                if request.user.username in prof_avec_colles:
                    groupe=Group.objects.get(name=prof_avec_colles[request.user.username])
                    tousleseleves=User.objects.filter(groups=groupe_eleves).order_by('username')
                    lesnotes={ joli_nom(item) : '' for item in tousleseleves}
                    notes=NotesColles.objects.filter(semaine=semaine,colleur__groups=groupe)
                    doublons={}
                    for x in notes:
                        if lesnotes[joli_nom(x.eleve)]=='':
                            lesnotes[joli_nom(x.eleve)]={"colleur":joli_nom(x.colleur),"note":x.note}
                        else:
                            if joli_nom(x.eleve) not in doublons: doublons[joli_nom(x.eleve)]=[]
                            doublons[joli_nom(x.eleve)].append({"colleur":joli_nom(x.colleur),"note":x.note})
                    response_data["lesnotes"]=lesnotes
                    response_data["doublons"]=doublons
            elif request.POST["colleur"]=="" and est_colleur(request.user):
                # un colleur récupère ses colles pour la semaine
                notessemaine={}
                autresnotes={}                
                notes=NotesColles.objects.filter(semaine=semaine,colleur=request.user)
                creneaux=CreneauxColleurs.objects.filter(colleur=request.user)
                groupes=Colloscope.objects.filter(semaine=semaine,creneau__in=creneaux)
                for item in groupes:
                    notessemaine[item.groupe.numero]=[]
                    for eleve in item.groupe.eleves.all().order_by("username"):
                        try:
                            lanote=notes.get(eleve=User.objects.get(username=eleve.username))
                            notessemaine[item.groupe.numero].append({"user":eleve.username,"eleve":joli_nom(eleve),"note":lanote.note})
                        except:
                            notessemaine[item.groupe.numero].append({"user":eleve.username,"eleve":joli_nom(eleve),"note":''})
                for eleve in User.objects.filter(groups=groupe_eleves).order_by("username"):
                    # ici on remet tout le monde et javascript gère ça facilement
                        try:
                            lanote=notes.get(eleve=eleve)
                            autresnotes[eleve.username]={"eleve":joli_nom(eleve),"note":lanote.note}
                        except:
                            autresnotes[eleve.username]={"eleve":joli_nom(eleve),"note":''}
                response_data["notessemaine"]=notessemaine
                response_data["autresnotes"]=autresnotes
            else:
                # un gestionnaire récupère les notes d'un colleur
                # quasiment la même chose que le else précédent : 
                # à mettre en fonction
                notessemaine={}
                autresnotes={}   
                colleur_name=request.POST["colleur"]   
                if est_gestionnaire_colle(request.user,colleur_name): 
                    colleur=User.objects.get(username=colleur_name)         
                    notes=NotesColles.objects.filter(semaine=semaine,colleur=colleur)
                    creneaux=CreneauxColleurs.objects.filter(colleur=colleur)
                    groupes=Colloscope.objects.filter(semaine=semaine,creneau__in=creneaux)
                    for item in groupes:
                        notessemaine[item.groupe.numero]=[]
                        for eleve in item.groupe.eleves.all().order_by("username"):
                            try:
                                lanote=notes.get(eleve=User.objects.get(username=eleve.username))
                                notessemaine[item.groupe.numero].append({"user":eleve.username,"eleve":joli_nom(eleve),"note":lanote.note})
                            except:
                                notessemaine[item.groupe.numero].append({"user":eleve.username,"eleve":joli_nom(eleve),"note":''})
                    for eleve in User.objects.filter(groups=groupe_eleves).order_by("username"):
                    # ici on remet tout le monde et javascript gère ça facilement
                            try:
                                lanote=notes.get(eleve=eleve)
                                autresnotes[eleve.username]={"eleve":joli_nom(eleve),"note":lanote.note}
                            except:
                                autresnotes[eleve.username]={"eleve":joli_nom(eleve),"note":''}
                    response_data["notessemaine"]=notessemaine
                    response_data["autresnotes"]=autresnotes
    except:
        print("erreur")
    return HttpResponse(json.dumps(response_data), content_type="application/json")    

def recuperation_informations_home(request):
    response_data = {}
    try:
        lesgroupes=request.user.groups.all()
        if groupe_eleves in lesgroupes:
            lasemaine=Semaines.objects.get(numero=request.POST["semaine"])  
            if lasemaine.numero<16: 
                groupe=GroupeColles.objects.get(eleves=request.user,numero__lte=19)
            else:
                groupe=GroupeColles.objects.get(eleves=request.user,numero__gte=20)
            try:
                msg=info_page_accueil(request.user,groupe,lasemaine)
            except:
                msg=[]
            response_data["informations"]=msg
    except:
        print("erreur")
    return HttpResponse(json.dumps(response_data), content_type="application/json")    

def modification_choix_option(request):
    response_data={}
    try:
        if request.method=="POST" and "choixoption" in request.POST:
            choix=request.POST["choixoption"]
            if choix in ["X","I","S","T"]:
                obj=Renseignements.objects.get(login=request.user.username,année=annee_courante)
                obj.option=choix
                obj.save()
    except:
        print("erreur")
    return HttpResponse(json.dumps(response_data), content_type="application/json")    

def modification_choix_orientation(request):
    response_data={}
    try:
        if request.method=="POST":
            if "choix1" in request.POST:
                choix=request.POST["choix1"]
                if choix in ["X","A","B","C","D","E"]:
                    obj=Renseignements.objects.get(login=request.user.username,année=annee_courante)
                    obj.choix1=choix
                    obj.save()
            elif "choix2" in request.POST:
                choix=request.POST["choix2"]
                if choix in ["X","A","B","C","D","E"]:
                    obj=Renseignements.objects.get(login=request.user.username,année=annee_courante)
                    obj.choix2=choix
                    obj.save()
            elif "choix3" in request.POST:
                choix=request.POST["choix3"]
                if choix in ["X","A","B","C","D","E"]:
                    obj=Renseignements.objects.get(login=request.user.username,année=annee_courante)
                    obj.choix3=choix
                    obj.save()                    
            elif "choix4" in request.POST:
                choix=request.POST["choix4"]
                if choix in ["X","A","B","C","D","E"]:
                    obj=Renseignements.objects.get(login=request.user.username,année=annee_courante)
                    obj.choix4=choix
                    obj.save()
    except:
        print("erreur")
    return HttpResponse(json.dumps(response_data), content_type="application/json")   

def download(request,letype,pk):
    def extension(nomfichier):
        l=nomfichier.split(".")
        if len(l)==1:
            return ""
        return "."+l[-1]
    def aux(nomfichier):  # pour enlever les caractères bizarres !
        res=""
        for x in nomfichier:
            if ord(x)<256:
                res+=x
        return res
    if letype=="file":
        try : 
            obj=Fichier.objects.get(id=pk)
            if autorise_menu(request.user,obj.menu):
                document = open('private_files/fichiers/'+str(pk)+extension(obj.nomfichier),'rb')
                response = HttpResponse(FileWrapper(document),content_type='application/octet-stream')
                response['Content-Disposition'] = 'attachment; filename="'+aux(obj.nomfichier)+'"'
                return response
        except: #fichier absent avec icone téléchargement?
            return redirect('/home')
    if letype=='prog':
        try:
            obj=ProgColleMath.objects.get(id=pk)
            document = open('private_files/prog_math/prog'+str(pk)+'.pdf','rb')
            response = HttpResponse(FileWrapper(document),content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename="prog'+str(obj.numero)+'.pdf"'
            return response
        except: #fichier absent avec icone téléchargement?
            return redirect('/home')
    if letype=='exos':
        try:
            obj=ProgColleMath.objects.get(id=pk)
            document = open('private_files/prog_math/exos'+str(pk)+'.pdf','rb')
            response = HttpResponse(FileWrapper(document),content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename="exos'+str(obj.numero)+'.pdf"'
            return response
        except: #fichier absent avec icone téléchargement?
            return redirect('/home')
    return redirect('/home')

def download_pronote(request):
    print(request.user.username)
    if request.user.username in prof_avec_colles:
            document = open('private_files/'+request.user.username+'.txt','rb')
            response = HttpResponse(FileWrapper(document),content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename="'+request.user.username+'.txt"'
            return response
    return redirect('/home')

