from stat import FILE_ATTRIBUTE_SPARSE_FILE
from .models import GestionDossier
from django.forms import ModelForm
from django import forms
from django.db import models
from django.contrib.auth.models import Group, User

class GestionDossierForm(ModelForm):
    class Meta:
        model=GestionDossier
        fields = '__all__'
