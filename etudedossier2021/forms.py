from stat import FILE_ATTRIBUTE_SPARSE_FILE
from .models import GestionDossier2021
from django.forms import ModelForm
from django import forms
from django.db import models
from django.contrib.auth.models import Group, User

class GestionDossier2021Form(ModelForm):
    class Meta:
        model=GestionDossier2021
        fields = '__all__'
