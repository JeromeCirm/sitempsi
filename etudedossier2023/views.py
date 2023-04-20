from django.shortcuts import render,redirect
from .parametres import rang_final,rang_fin_phase,sauvegarde_phase_generale,lire_un_dossier,lire_tous_les_dossiers,prepare_selection,convertion_excel,convertion_xslx,maj_dossier,patch
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate, login
from .forms import GestionDossier2023Form
from .models import GestionDossier2023
from os import remove
import base64
from json import loads
from base.fonctions import auth

groupe_etudedossier=Group.objects.get(name='etudedossier')

@auth([groupe_etudedossier])
def selection(request,err=False):
    context={}
    prepare_selection(context,request)
    if err:
        context['erreur']="oui"
    return render(request,'etudedossier2023/selection.html',context)

@auth([groupe_etudedossier])
def affichage(request):
    context={}
    lire_tous_les_dossiers(request,context)
    return render(request,'etudedossier2023/affichage.html',context)

@auth([groupe_etudedossier])
def traitement(request):
    context={}
    if request.method=='POST':
        if "NoteAChanger" in request.POST and request.POST["NoteAChanger"]=="true":
            maj_dossier(request)
    if lire_un_dossier(request,context):
        return render(request,'etudedossier2023/traitement.html',context)
    else:
        return selection(request,err=True)

@auth([groupe_etudedossier])
def gestion(request):
    context={}
    form=GestionDossier2023Form()
    if request.method=='POST' and (request.user.username in ["nizon","rezzouk"]):
        if request.POST["valeur"]=='upload_initial':
            old=GestionDossier2023.objects.all()
            for x in old:
                x.fichier_initial.delete()
                x.delete()
            try:
                remove('etudedossier2023/stockage/fichierinitial.xlsx')
            except:
                pass
            form=GestionDossier2023Form(request.POST,request.FILES) 
            if form.is_valid():
                form.save()
                context["message"]="fichier uploadé"
        if request.POST["valeur"]=='convertir_excel':
            #convertion_excel()
            context["message"]="convertion de début de phase inactive en ce moment !" #réalisée"
        if request.POST["valeur"]=='sauvegarde_generale':
            sauvegarde_phase_generale()
            context["message"]="sauvegarde fin de phase générale effectuée"
        if request.POST["valeur"]=='rang_fin_phase':
            rang_fin_phase()
            context["message"]="rang de fin de phase générale créé en favorisant les catégories"
        if request.POST["valeur"]=='rang_final':
            rang_final()
            context["message"]="rang final créé en favorisant les catégories sans égalité"
        if request.POST["valeur"]=='creation_excel':
            convertion_xslx()
            context["message"]="convertion vers xlsx terminée"
    context["form"]=form
    return render(request,'etudedossier2023/gestion.html',context)

@auth([groupe_etudedossier])
def download(request,nom):
    try:
        if nom=='fichierfinal.xlsx':
            document=open('etudedossier2023/stockage/fichierfinal.xlsx','rb')
        else:
            nom=nom[2:-1].encode()
            nom=(base64.b64decode(nom)).decode("utf-8")
            document=open('etudedossier2023/fiches/'+nom,'rb')
        response = HttpResponse(FileWrapper(document),content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="'+nom+'"'
        return response    
    except:
        return HttpResponse("impossible de trouver le fichier")
