# fonctions spécifique à la gestion de classe
# colloscope/trombi/emploi du temps/etc
from django.shortcuts import render,redirect

from .generic import *
from .donnees_classe import *
from .special_jerome import *
from .forms import FichierFormFichier,RenseignementsForm
from django.db.models import Max
import datetime
try:
    from .hors_git.fonctions_hors_git import * 
except:
    print("pas d'hors-git trouvé")
    pass

liste_classe=['gestion_jerome','trombinoscope','emploi_du_temps','contacts','colloscope_s1','colloscope_s2',
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
        if request.POST['action']=='creation_creneaux_colles_s2':
            creation_creneaux_colles_s2(context)
        if request.POST['action']=='creation_colloscope':
            creation_colloscope(context)
        if request.POST['action']=='creation_colloscope_s2':
            creation_colloscope_s2(context)
        if request.POST['action']=='export_renseignements':
            export_renseignements(context)
        if request.POST['action']=='export_renseignements_v2':
            export_renseignements_v2(context)
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
    lessemaines=Semaines.objects.filter(numero__lte=15).order_by('numero')
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
    context["colleurmath"]=CreneauxColleurs.objects.filter(matière="math",numero__lte=20).order_by('numero')
    context["colleurphysique"]=CreneauxColleurs.objects.filter(matière="physique",numero__lte=20).order_by('numero')
    context["colleuranglais"]=CreneauxColleurs.objects.filter(matière="anglais",numero__lte=20).order_by('numero')
    try:
        context["colloscope_informations"]=colloscope_informations()
    except:
        context["colloscope_informations"]=[]
    return render(request,'gestionmenu/colloscope.html',context)

def colloscope_s2(request,id_menu,context):
    lesgroupes=GroupeColles.objects.filter(numero__gte=20).order_by('numero')
    lessemaines=Semaines.objects.filter(numero__gte=16).order_by('numero')
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
                    math=str(colle.creneau.numero-20)
                if colle.creneau.matière=="physique":
                    physique="-"+chr(64+colle.creneau.numero-20)
                if colle.creneau.matière=="anglais":
                    anglais="-"+chr(96+colle.creneau.numero-20)
            ligne.append(math+physique+anglais)
        tableau.append({"semaine" : {"numero":semaine.numero,"date":date_fr(semaine.date,True)},"ligne" : ligne})
    context["tableau"]=tableau
    context["lesgroupes"]=lesgroupes
    context["colleurmath"]=CreneauxColleurs.objects.filter(matière="math",numero__gte=20).order_by('numero')
    context["colleurphysique"]=CreneauxColleurs.objects.filter(matière="physique",numero__gte=20).order_by('numero')
    context["colleuranglais"]=CreneauxColleurs.objects.filter(matière="anglais",numero__gte=20).order_by('numero')
    try:
        context["colloscope_informations"]=colloscope_informations()
    except:
        context["colloscope_informations"]=[]
    return render(request,'gestionmenu/colloscope2.html',context)

def programme_colle_math(request,id_menu,context):
    # attention, ne doit apparaitre qu'une seule fois dans le menu !
    # sinon problème pour connaitre le gestionnaire
    progs=ProgColleMath.objects.values()
    context["contenu"]=progs
    context['gestionnaire']=est_gestionnaire_menu(request.user,Menu.objects.get(id=id_menu))
    return render(request,'gestionmenu/prog_colles_math.html',context)

def lire_notes_colles(request,id_menu,context):
    lesnotes=NotesColles.objects.filter(eleve=request.user).order_by("-semaine")
    context["contenu"]=[{"semaine":item.semaine,"note":item.note,"colleur":joli_nom(item.colleur)} for item in lesnotes]
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
        if not (JOLI_NOM): context["msg"]="Ne pas oublier de valider les modifications si besoin : "
        if request.method=="POST" and not (JOLI_NOM):
            form=RenseignementsForm(request.POST,instance=obj)
            if form.is_valid():
                form.save()
                request.user.email=request.POST["mail"]
                if not (JOLI_NOM):
                    request.user.first_name=request.POST["prenomusage"]
                    request.user.last_name=request.POST["nomusage"]
                request.user.save()
                context["msg"]="modifications enregistrées ! "
                context['form']=form
                context["mail"]=request.user.email
                context["prenomusage"]=request.user.first_name
                context["nomusage"]=request.user.last_name                
                return render(request,'gestionmenu/fiche_renseignements.html',context)
            context["msg"]="erreur dans le formulaire"
        form=RenseignementsForm(instance=obj)
        context['form']=form
        context["mail"]=request.user.email
        context["prenomusage"]=request.user.first_name
        context["nomusage"]=request.user.last_name
        if affiche_choix_option:
            context["choixoption"]=obj.option
            context["affiche_choix_option"]=True
        if affiche_choix_orientation:
            context["choix1"]=obj.choix1
            context["choix2"]=obj.choix2
            context["choix3"]=obj.choix3
            context["choix4"]=obj.choix4
            context["affiche_choix_orientation"]=True
    except:
        return redirect('/home')
    context["jolinom"]=JOLI_NOM
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
    if request.user.username in prof_avec_colles:
        liste_colleurs=User.objects.filter(groups=Group.objects.get(name=prof_avec_colles[request.user.username]))
    else:
        return redirect('/home/')
    semaines=Semaines.objects.all().order_by("numero")
    if request.method=="POST":
        semainedep=int(request.POST["semainedep"])
        try:
            semainedep=Semaines.objects.get(numero=semainedep)
        except:
            semainedep=semaines.first()
        semainefin=int(request.POST["semainefin"])
        try:
            semainefin=Semaines.objects.get(numero=semainefin)
        except:
            semainefin=semaines.last()
        if request.POST["quinzaine"]=="oui":
            quinzaine=True
        else : 
            quinzaine=False
        leseleves=User.objects.filter(groups=groupe_eleves).order_by("username")
        if quinzaine : 
            ecart=2
        else : 
            ecart=1
        txt="Nom;prenom"
        for _ in range(semainedep.numero,semainefin.numero+1,ecart):
            txt+=";20"
        txt+="\n"
        enplus=[]
        for user in leseleves:
            txt+=dic_pronote[user.username]
            for lasemaine in range(semainedep.numero,semainefin.numero+1,ecart):
                txt+=";"
                lesnotes=NotesColles.objects.filter(colleur__in=liste_colleurs,semaine__numero__gte=lasemaine,
                semaine__numero__lte=min(semainefin.numero,lasemaine+ecart-1),eleve=user)
                if len(lesnotes)>0:
                    txt+=str(lesnotes[0].note)
                if len(lesnotes)>1:
                    enplus+=lesnotes[1:]
            txt+="\n"
        txt.encode('latin1')
        sortie=open('private_files/'+request.user.username+'.txt',"w",encoding="latin1")
        sortie.write(txt)
        sortie.close()
        context["enplus"]=enplus
        context["fichier"]=request.user.username+'.txt'
    else :
        semainedep=semaines.first()
        semainefin=semaines.last()
        quinzaine=False
    context["semaines"]=semaines
    context["semainedep"]=semainedep
    context["semainefin"]=semainefin
    context["quinzaine"]=quinzaine
    return render(request,'gestionmenu/creation_pronote.html',context)
    
