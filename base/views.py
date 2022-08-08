from django.shortcuts import render,redirect
from django.contrib.auth import logout
from .fonctions import *

def auth(group_list=[]):
    def teste(func):
        def nouvelle_func(request,*args,**kwargs):
            if request.user.is_authenticated:
                if group_list==[]:
                    return func(request,*args,**kwargs)
                lesgroupes=request.user.groups.all()
                for x in group_list:
                    if x in lesgroupes:
                        return func(request,*args,**kwargs)
            return connexion(request)
        return nouvelle_func
    return teste

def connexion(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None: 
            # on vérifie si le compte a bien été activé
            try:
                utilisateur=Utilisateur.objects.get(user=user)
                if not utilisateur.en_attente_confirmation:
                    login(request,user)
                    return redirect('creneaux')
                #compte en attente si on arrive ici
            except:
                pass
    context={}
    return render(request,'base/connexion.html',context)

def deconnexion(request):
    logout(request)
    return redirect('')

def creation_compte(request):
    context={}
    if request.method=="POST":
        reussi,err=demande_creation_compte(request)
        if reussi:
            context["reussi"]=True
        else:
            context["echec"]=True
            context["err"]=err
            context["ancien"]=request.POST
    return render(request,'base/creation_compte.html',context)

def validation_compte(request,login=None,lehash=None):
    if login==None:
        context={ "msg" : "Le lien n'est pas valide"}
    else:
        context={ "msg" : verifie_lien_validation(login,lehash)}
    return render(request,'base/validation_compte.html',context)

def recuperation_password(request):
    context={}
    if request.method=="POST":   
        context["msg"]=envoie_mail_recuperation_mot_de_passe(request)
    return render(request,'base/recuperation_password.html',context)

def demande_reinitialisation(request,login=None,lehash=None):
    if request.method=='POST':
        # print("here")
        context={**reinitialise_mot_de_passe(request)}
    elif login==None:
        context={ "msg" : "Le lien n'est pas valide"}
    else:
        context={ **verifie_lien_reinitialisation(login,lehash)}
    return render(request,'base/demande_reinitialisation.html',context)

def home(request):
    context={}
    #envoie_mail(['jerome.99@hotmail.fr'],'test',' premier envoi de mail')
    return render(request,'base/home.html',context)