# fonctions spécifique à la gestion de classe
# colloscope/trombi/emploi du temps/etc
from django.shortcuts import render,redirect
from django.contrib.auth.models import Group

from .generic import est_gestionnaire_menu
from .donnees_classe import *
from .special_jerome import *
from .forms import FichierFormFichier,RenseignementsForm

liste_classe=['gestion_jerome','trombinoscope','emploi_du_temps','contacts','colloscope_s1',
'programme_colle_math','rentrer_notes_colles','lire_notes_colles','lire_notes_colleurs',
'modifier_notes_colleurs','lire_fiches_eleves','fiche_renseignements',
'creation_fichier_pronote']
groupe_eleves=Group.objects.get(name='eleves')
groupe_profs=Group.objects.get(name='profs')
groupe_colleurs_math=Group.objects.get(name='colleurs_math')
groupe_colleurs_physique=Group.objects.get(name='colleurs_physique')
groupe_colleurs_anglais=Group.objects.get(name='colleurs_anglais')
groupe_colleurs_philo=Group.objects.get(name='colleurs_philo')

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
        tableau.append({"semaine" : semaine,"ligne" : ligne})
    context["tableau"]=tableau
    context["lesgroupes"]=lesgroupes
    context["colleurmath"]=CreneauxColleurs.objects.filter(matière="math").order_by('numero')
    context["colleurphysique"]=CreneauxColleurs.objects.filter(matière="physique").order_by('numero')
    context["colleuranglais"]=CreneauxColleurs.objects.filter(matière="anglais").order_by('numero')
    return render(request,'gestionmenu/colloscope.html',context)

def programme_colle_math(request,id_menu,context):
    context["msg"]="programme_colle_math"
    return render(request,'gestionmenu/home.html',context)

def rentrer_notes_colles(request,id_menu,context):
    context["msg"]="rentrer_notes_colles"
    return render(request,'gestionmenu/home.html',context)

def lire_notes_colles(request,id_menu,context):
    context["msg"]="lire_notes_colles"
    return render(request,'gestionmenu/home.html',context)

def lire_notes_colleurs(request,id_menu,context):
    context["msg"]="lire_notes_colleurs"
    return render(request,'gestionmenu/home.html',context)

def modifier_notes_colleurs(request,id_menu,context):
    context["msg"]="modifier_notes_colleurs"
    return render(request,'gestionmenu/home.html',context)

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
        if True: #try:
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
        #except:
            pass
    return render(request,'gestionmenu/lire_renseignements.html',context)

def fiche_renseignements(request,id_menu,context):
    try:
        obj=Renseignements.objects.get(login=request.user.username,année=annee_courante)
        if request.method=="POST":
            form=RenseignementsForm(request.POST,instance=obj)
            if form.is_valid():
                form.save()
                context["msg"]="modifications enregistrées ! "
                context['form']=form
                return render(request,'gestionmenu/fiche_renseignements.html',context)
        form=RenseignementsForm(instance=obj)
        context['form']=form
        context["msg"]="Ne pas oublier de valider les modifications si besoin : "
    except:
        return redirect('/home')
    return render(request,'gestionmenu/fiche_renseignements.html',context)

def creation_fichier_pronote(request,id_menu,context):
    context["msg"]="creation_fichier_pronote"
    return render(request,'gestionmenu/home.html',context)
    
