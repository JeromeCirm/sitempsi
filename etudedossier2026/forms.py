from stat import FILE_ATTRIBUTE_SPARSE_FILE
from .models import GestionDossier2026
from django.forms import ModelForm
from django import forms
from django.db import models
from django.contrib.auth.models import Group, User

class GestionDossier2026Form(ModelForm):
    class Meta:
        model=GestionDossier2026
        fields = '__all__'
