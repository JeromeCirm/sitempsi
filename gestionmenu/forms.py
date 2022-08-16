from django.forms import ModelForm
from .models import Fichier,Renseignements,Menu
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
        exclude=('login','année','option','choix1','choix2','choix3','choix4','pdf')

class MenuForm(ModelForm):
    type_de_menu=forms.ChoiceField(choices=[('l','liste de fichiers'),('f','fichier unique')])
    class Meta:
        model=Menu
        fields=['nom']

class MenuFormSimple(ModelForm):
    class Meta:
        model=Menu
        fields=['nom']
