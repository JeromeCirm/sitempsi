from django.forms import ModelForm
from .models import Fichier,Renseignements,Menu,ProgColleMath
from django import forms
from django.contrib.auth.models import Group, User

class FichierForm(ModelForm):
    class Meta:
        model=Fichier
        fields=['description','fichier']

class FichierUniqueForm(ModelForm):
    class Meta:
        model=Fichier
        fields=['fichier']

class FichierFormDescription(ModelForm):
    class Meta:
        model=Fichier
        fields=['description']

class FichierFormFichier(ModelForm):
    class Meta:
        model=Fichier
        fields=['fichier']

class RenseignementsForm(ModelForm):
    class Meta:
        model=Renseignements
        fields = '__all__'
        labels= {
            "nomusage" : "Nom d'usage",
            "prenomusage" : "Prénom d'usage",
            "naissance" : "Date de naissance",
            "tempstrajet" : "Temps de trajet Lycée-domicile (aller)",
            "seullogement" : "Es-tu seul(e) dans ton logement ?",
            "motivationprepa" : "Pourquoi avoir choisi MPSI?",
            "lyceeorigine" : "Nom du lycée d'origine",
            "villelyceeorigine" : "Ville du lycée d'origine",
            "professionparents" : "Professions des parents",
            "freressoeurs" : "Renseignements sur les frères/soeurs",
            "calculatrice" : "Type de calculatrice utilisée",
            "accessordinateur" : "as-tu accès à un ordinateur personnel ?",
            "connexioninternet" : "as-tu possibilité de te connecter régulièrement à internet ?"
        }
        exclude=('nomusage','prenomusage','login','année','option','pdf')

class MenuForm(ModelForm):
    type_de_menu=forms.ChoiceField(choices=[('l','liste de fichiers'),('f','fichier unique')])
    class Meta:
        model=Menu
        fields=['nom']

class MenuFormSimple(ModelForm):
    class Meta:
        model=Menu
        fields=['nom']

class ProgColleMathForm(ModelForm):
    class Meta:
        model=ProgColleMath
        fields=['numero','description','programme','exercices'] 

class ProgColleMathFormDescription(ModelForm):
    class Meta:
        model=ProgColleMath
        fields=['numero','description'] 

class ProgColleMathFormProgramme(ModelForm):
    class Meta:
        model=ProgColleMath
        fields=['programme'] 

class ProgColleMathFormExercices(ModelForm):
    class Meta:
        model=ProgColleMath
        fields=['exercices'] 