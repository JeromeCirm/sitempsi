# fonctions spécifique à la gestion de classe
# colloscope/trombi/emploi du temps/etc
from django.shortcuts import render,redirect

from .generic import *
from .donnees_classe import *
from .special_jerome import *
from .forms import FichierFormFichier,RenseignementsForm
from django.db.models import Max
import datetime

liste_classe=['gestion_jerome','trombinoscope','emploi_du_temps','contacts','colloscope_s1',
'programme_colle_math','rentrer_notes_colles','lire_notes_colles','lire_notes_colleurs',
'modifier_notes_colleurs','lire_fiches_eleves','fiche_renseignements',
'creation_fichier_pronote','lien_bashton']

def gestion_jerome(request,id_menu,context):
    if request.method=='POST':
        if request.POST['action']=='maj_comptes_profs':
            maj_comptes_profs(context)
        if request.POST['action']=='reinitialisation_eleves':
            reinitialisation_eleves(context)
        if request.POST['action']=='maj_comptes_colleurs':
            maj_comptes_colleurs(context)
        if request.POST['action']=='creation_groupes_colles_s1':
            creation_groupes_colles_s1(context)
        if request.POST['action']=='creation_groupes_colles_s2':
            creation_groupes_colles_s2(context)
        if request.POST['action']=='creation_creneaux_colles':
            creation_creneaux_colles(context)
        if request.POST['action']=='creation_colloscope':
            creation_colloscope(context)
        if request.POST['action']=='export_renseignements':
            export_renseignements(context)
    return render(request,'gestionmenu/gestion_jerome.html',context)

def contacts(request,id_menu,context):
    usergroupes=request.user.groups.all()
    paseleves=[groupe_colleurs_math,groupe_colleurs_physique,
        groupe_colleurs_anglais,groupe_colleurs_philo,groupe_profs]
    if groupe_eleves in usergroupes:
        context["profs"]=User.objects.filter(groups__in=paseleves).distinct().order_by("username")
    print(set(paseleves))
    print(set(usergroupes))
    print(set(paseleves)&set(usergroupes))
    if set(paseleves)&set(usergroupes)!=set():
        context["eleves"]=GroupeColles.objects.all().order_by('numero')
    return render(request,'gestionmenu/contacts.html',context)

def colloscope_s1(request,id_menu,context):
    lesgroupes=GroupeColles.objects.filter(numero__lte=16).order_by('numero')
    lessemaines=Semaines.objects.filter(numero__lte=16).order_by('numero')
    tableau=[] # le tableau des colles, une ligne par semaine
    for semaine in lessemaines:
        ligne=[]
        for groupe in lesgroupes:
            math=""
            physique=""
            anglais=""
            lescolles=Colloscope.objects.filter(semaine=semaine,groupe=groupe)
            for colle in lescolles:
                if colle.creneau.matière=="math":
                    math=str(colle.creneau.numero)
                if colle.creneau.matière=="physique":
                    physique="-"+chr(64+colle.creneau.numero)
                if colle.creneau.matière=="anglais":
                    anglais="-"+chr(96+colle.creneau.numero)
            ligne.append(math+physique+anglais)
        tableau.append({"semaine" : {"numero":semaine.numero,"date":date_fr(semaine.date,True)},"ligne" : ligne})
    context["tableau"]=tableau
    context["lesgroupes"]=lesgroupes
    context["colleurmath"]=CreneauxColleurs.objects.filter(matière="math").order_by('numero')
    context["colleurphysique"]=CreneauxColleurs.objects.filter(matière="physique").order_by('numero')
    context["colleuranglais"]=CreneauxColleurs.objects.filter(matière="anglais").order_by('numero')
    return render(request,'gestionmenu/colloscope.html',context)

def programme_colle_math(request,id_menu,context):
    # attention, ne doit apparaitre qu'une seule fois dans le menu !
    # sinon problème pour connaitre le gestionnaire
    progs=ProgColleMath.objects.values()
    context["contenu"]=progs
    context['gestionnaire']=est_gestionnaire_menu(request.user,Menu.objects.get(id=id_menu))
    return render(request,'gestionmenu/prog_colles_math.html',context)

def lire_notes_colles(request,id_menu,context):
    context["contenu"]=NotesColles.objects.filter(eleve=request.user).order_by("-semaine")
    return render(request,'gestionmenu/lire_notes_colles.html',context)

def lire_notes_colleurs(request,id_menu,context):
    if request.user.username not in prof_avec_colles:
        return redirect('/home')
    context["semaine"]=semaine_en_cours() 
    lessemaines=Semaines.objects.all().order_by("numero")
    context["lessemaines"]=[{"numero":x.numero,"date":date_fr(x.date,True)} for x in lessemaines]
    return render(request,'gestionmenu/notes_colles_semaine.html',context)

def rentrer_notes_colles(request,id_menu,context):
    context["semaine"]=semaine_en_cours() 
    lessemaines=Semaines.objects.all().order_by("numero")
    context["lessemaines"]=[{"numero":x.numero,"date":date_fr(x.date,True)} for x in lessemaines]
    return render(request,'gestionmenu/rentrer_notes_colles.html',context)

def modifier_notes_colleurs(request,id_menu,context):
    if request.user.username in prof_avec_colles:
        groupe=Group.objects.get(name=prof_avec_colles[request.user.username])
        context["listecolleurs"]=User.objects.filter(groups=groupe).order_by("username")
    else:
        return redirect('/home')
    context["semaine"]=semaine_en_cours() 
    lessemaines=Semaines.objects.all().order_by("numero")
    context["lessemaines"]=[{"numero":x.numero,"date":date_fr(x.date,True)} for x in lessemaines]
    return render(request,'gestionmenu/rentrer_notes_colles.html',context)

def lire_fiches_eleves(request,id_menu,context):
    annee=annee_courante
    if affiche_choix_orientation:
        context["orientation"]=True
        context["mps"]=len(Renseignements.objects.filter(choix1='A',année=annee))
        context["mp"]=len(Renseignements.objects.filter(choix1='B',année=annee))
        context["psis"]=len(Renseignements.objects.filter(choix1='C',année=annee))
        context["psi"]=len(Renseignements.objects.filter(choix1='D',année=annee))
        context["reo"]=len(Renseignements.objects.filter(choix1='E',année=annee))
        context["mpslist"]=Renseignements.objects.filter(choix1='A',année=annee)
        context["mplist"]=Renseignements.objects.filter(choix1='B',année=annee)
        context["psislist"]=Renseignements.objects.filter(choix1='C',année=annee)
        context["psilist"]=Renseignements.objects.filter(choix1='D',année=annee)
        context["reolist"]=Renseignements.objects.filter(choix1='E',année=annee)
        context["sanschoix"]=len(User.objects.filter(groups=groupe_eleves))-context["mps"]-context["mp"]-context["psis"]-context["psi"]-context["reo"]
        context["sanschoixlist"]=Renseignements.objects.filter(choix1=None,année=annee)
    if affiche_choix_option:
        context["option"]=True
        context["optioninfo"]=len(Renseignements.objects.filter(option='I',année=annee))
        context["optionsi"]=len(Renseignements.objects.filter(option='S',année=annee))
        context["optiontp"]=len(Renseignements.objects.filter(option='T',année=annee))
        context["optionrien"]=len(User.objects.filter(groups=groupe_eleves))-context["optioninfo"]-context["optionsi"]-context["optiontp"]
        context["optioninfolist"]=Renseignements.objects.filter(option='I',année=annee)
        context["optionsilist"]=Renseignements.objects.filter(option='S',année=annee)
        context["optiontplist"]=Renseignements.objects.filter(option='T',année=annee)
        context["optionrienlist"]=Renseignements.objects.filter(option=None,année=annee)
    context["annee"]=annee_courante
    context["selection"]="false"
    if request.method=="POST":
        try:
            context["selection"]="true"
            menu=Menu.objects.get(pk=id_menu)
            login=request.POST['eleve']
            context['login']=login
            annee=int(request.POST['annee'])
            context["annee"]=annee
            eleve=Renseignements.objects.get(login=login,année=annee)
            if request.POST["action"]=='ajout' and est_gestionnaire_menu(request.user,menu):
                if 'fichier' in request.FILES:
                    obj=Fichier.objects.create(description="bidon",ordre=0,menu=menu)
                    form=FichierFormFichier(request.POST,request.FILES,instance=obj)
                    if form.is_valid():
                        new_fichier=form.save(commit=False)
                        new_fichier.nomfichier=request.FILES['fichier']
                        new_fichier.save()
                        eleve.pdf.add(new_fichier)
                        return redirect('/menu/'+str(menu.id))
                context["eleve"]=request.POST['eleve']
                form=FichierFormFichier()
                context["form"]=form
                return render(request,'gestionmenu/ajout_fichier_parcoursup.html',context)
            donnees=RenseignementsForm(instance=eleve)
            context["donnees"]=donnees
            context["gestionnaire"]=est_gestionnaire_menu(request.user,menu=menu)
            context["pdf"]=eleve.pdf
            if context["annee"]==annee_courante:
                try:
                    user=User.objects.get(username=login)
                    context["mail"]=user.email
                except:
                    pass
        except:
            pass
    return render(request,'gestionmenu/lire_renseignements.html',context)

def fiche_renseignements(request,id_menu,context):
    try:
        obj=Renseignements.objects.get(login=request.user.username,année=annee_courante)
        context["msg"]="Ne pas oublier de valider les modifications si besoin : "
        if request.method=="POST":
            form=RenseignementsForm(request.POST,instance=obj)
            if form.is_valid():
                form.save()
                request.user.email=request.POST["mail"]
                request.user.first_name=request.POST["prenomusage"]
                request.user.last_name=request.POST["nomusage"]
                request.user.save()
                context["msg"]="modifications enregistrées ! "
                context['form']=form
                context["mail"]=request.user.email
                return render(request,'gestionmenu/fiche_renseignements.html',context)
            context["msg"]="erreur dans le formulaire"
        form=RenseignementsForm(instance=obj)
        context['form']=form
        context["mail"]=request.user.email
    except:
        return redirect('/home')
    return render(request,'gestionmenu/fiche_renseignements.html',context)

def semaine_en_cours():
    # cherche la semaine en cours. Renvoi la première sinon
    try:
        semaine=Semaines.objects.filter(date__lte=datetime.date.today()).order_by('-date')
        if len(semaine)>0:
            # on renvoie la dernière semaine commençant avant aujourd'hui
            return semaine[0]
        else:
            # on renvoie la première semaine
            semaine=Semaines.objects.all().order_by('date')
            return semaine[0]
    except:
        # pas de semaines créées pour l'instant
        return None

def informations_semaine(request):
    # renvoie une list de messages à afficher concernant les colles de la semaine, les TD, etc.. de l'éleve
    semaine=semaine_en_cours() # on récupère la semaine en cours
    groupe=GroupeColles.objects.get(eleves=request.user)
    colles=Colloscope.objects.filter(semaine=semaine,groupe=groupe)
    msg=[]
    for x in colles:
        msg.append("colle de "+x.creneau.matière+" avec "+x.creneau.colleur.username+" "+x.creneau.jour+" à "+x.creneau.horaire+" en "+x.creneau.salle)
    return msg 

def creation_fichier_pronote(request,id_menu,context):
    context["msg"]="creation_fichier_pronote"
    return render(request,'gestionmenu/home.html',context)
    
