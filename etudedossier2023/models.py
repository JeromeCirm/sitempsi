from operator import mod
from django.db import models
from django.contrib.auth.models import Group, User
# Create your models here.

class GestionDossier2023(models.Model):
    def upinit(self,filename):
        return 'etudedossier2023/stockage/fichierinitial.xlsx'
    fichier_initial=models.FileField(null=True,blank=True,upload_to=upinit)

class SauvegardeSelection2023(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    valeur=models.TextField(default="")
    ordre=models.TextField(default="")
    boursier=models.BooleanField(default=False)
    pasexpert=models.BooleanField(default=False)
    