from operator import mod
from django.db import models
from django.contrib.auth.models import Group, User
# Create your models here.

class GestionDossier2024(models.Model):
    def upinit(self,filename):
        return 'etudedossier2024/stockage/fichierinitial.xlsx'
    fichier_initial=models.FileField(null=True,blank=True,upload_to=upinit)

class SauvegardeSelection2024(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    valeur=models.TextField(default="")
    ordre=models.TextField(default="")
    boursier=models.BooleanField(default=False)
    pasexpert=models.BooleanField(default=False)

class AnciensEleves(models.Model):
    annee=models.TextField(default="")
    classe=models.TextField(default="")
    num_dossier=models.TextField(default="")
    rne=models.TextField(default="")
    prenom=models.TextField(default="")
    nom=models.TextField(default="")
    note_initiale=models.TextField(default="")
    note_finale=models.TextField(default="")
    rang=models.TextField(default="")
    modif_auto=models.TextField(default="")
    commentaire=models.TextField(default="")


    