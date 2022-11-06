from django.db import models
from django.contrib.auth.models import Group, User

class Menu(models.Model):
    nom=models.CharField(max_length=40)
    parent=models.IntegerField(blank=True)  # 0 pour un menu principal
    fonction=models.CharField(max_length=50,blank=True,default="")  #  fonction à appeler : vide s'il y des sous-menus
    groupes=models.ManyToManyField(Group,blank=True)
    gestionnaires=models.ManyToManyField(User,blank=True)
    ordre=models.IntegerField(default=0) # ordre dans le sous-menu

    def __str__(self):
        return self.nom+",id "+str(self.pk)+", parent "+str(self.parent)+",ordre "+str(self.ordre)+" "+str(self.fonction)

    class Meta : 
        ordering=['parent','ordre']

def extension(nomfichier):
    l=str(nomfichier).split(".")
    if len(l)==1:
        return ""
    return "."+l[-1]

class Fichier(models.Model):
    description=models.CharField(max_length=5000,default="",blank=True)
    def uploadpath(self,filename):
        return 'private_files/fichiers/'+str(self.id)+extension(self.nomfichier)
    fichier=models.FileField(null=True,blank=True,upload_to=uploadpath)
    nomfichier=models.CharField(max_length=100,null=True,blank=True)
    ordre=models.IntegerField(null=True,blank=True)
    menu=models.ForeignKey(Menu,on_delete=models.CASCADE,blank=True,null=True)
    date_parution=models.DateField(blank=True,null=True)

    def __str__(self):
        return str(self.nomfichier)+" : "+str(self.description)

    class Meta : 
        ordering=['-ordre']

class Semaines(models.Model):
    numero=models.IntegerField()
    date=models.DateField()

    def __str__(self):
        return str(self.numero)

class CreneauxColleurs(models.Model):
    colleur=models.ForeignKey(User,on_delete=models.CASCADE)
    jour=models.CharField(max_length=20,blank=True,default="")
    horaire=models.CharField(max_length=20,blank=True,default="")
    salle=models.CharField(max_length=20,blank=True,default="")
    matière=models.CharField(max_length=20,blank=True,default="")
    numero=models.IntegerField()

    def __str__(self):
        return self.colleur.username+": "+str(self.jour)+" "+str(self.horaire)

class GroupeColles(models.Model):
    numero=models.IntegerField()
    eleves=models.ManyToManyField(User)

    def __str__(self):
        return str(self.numero)

class Colloscope(models.Model):
    semaine=models.ForeignKey(Semaines,on_delete=models.CASCADE)
    groupe=models.ForeignKey(GroupeColles,on_delete=models.CASCADE)
    creneau=models.ForeignKey(CreneauxColleurs,on_delete=models.CASCADE)

class Divers(models.Model):
    label=models.CharField(max_length=30)
    contenu=models.TextField()
    
class Renseignements(models.Model):
    login=models.CharField(max_length=50)
    année=models.IntegerField(null=True,blank=True)
    nomusage=models.CharField(max_length=50,null=True,blank=True)
    prenomusage=models.CharField(max_length=50,null=True,blank=True)
    naissance=models.DateField(null=True,blank=True)
    tempstrajet=models.IntegerField(null=True,blank=True)
    seullogement=models.BooleanField(null=True,blank=True)
    motivationprepa=models.TextField(null=True,blank=True)
    lyceeorigine=models.CharField(max_length=50,null=True,blank=True)
    villelyceeorigine=models.CharField(max_length=50,null=True,blank=True)
    professionparents=models.TextField(null=True,blank=True)
    freressoeurs=models.TextField(null=True,blank=True)
    calculatrice=models.CharField(max_length=50,null=True,blank=True)
    accessordinateur=models.BooleanField(null=True,blank=True)
    connexioninternet=models.BooleanField(null=True,blank=True)
    evalcours=[['1','1 :quasi inexistant'],['2','2'],['3','3'],['4','4'],['5','5 : sans changement notable']]
    coursconfinementmath=models.CharField(max_length=1,choices=evalcours,null=True,blank=True)
    coursconfinementphysique=models.CharField(max_length=1,choices=evalcours,null=True,blank=True)
    confinementcommentaire=models.TextField(null=True,blank=True)
    notesbac=models.TextField(null=True,blank=True)
    def uploadpath(self,filename):
        return 'private_files/fichiers/'+str(self.id)+extension(self.nomfichier)
    pdf=models.ManyToManyField(Fichier)
    choix1=models.CharField(max_length=1,choices=[['A','MP*'],['B','MP'],['C','PSI*'],['D','PSI'],['E','Réorientation']],null=True,blank=True)
    choix2=models.CharField(max_length=1,choices=[['A','MP*'],['B','MP'],['C','PSI*'],['D','PSI'],['E','Réorientation']],null=True,blank=True)
    choix3=models.CharField(max_length=1,choices=[['A','MP*'],['B','MP'],['C','PSI*'],['D','PSI'],['E','Réorientation']],null=True,blank=True)
    choix4=models.CharField(max_length=1,choices=[['A','MP*'],['B','MP'],['C','PSI*'],['D','PSI'],['E','Réorientation']],null=True,blank=True)
    option=models.CharField(max_length=1,choices=[['I','Info'],['S','SI'],['T','SI avec TP']],null=True,blank=True)

class ProgColleMath(models.Model):
    numero=models.IntegerField()
    description=models.CharField(max_length=5000,default="")
    def uploadpathprog(self,filename):
        return 'private_files/prog_math/prog'+str(self.id)+'.pdf'
    def uploadpathexos(self,filename):
        return 'private_files/prog_math/exos'+str(self.id)+'.pdf'
    programme=models.FileField(null=True,blank=True,upload_to=uploadpathprog)
    exercices=models.FileField(null=True,blank=True,upload_to=uploadpathexos)

    class Meta : 
        ordering=['-numero']

class NotesColles(models.Model):
    colleur=models.ForeignKey(User,on_delete=models.CASCADE)
    eleve=models.ForeignKey(User,related_name='%(class)s_requests_created',on_delete=models.CASCADE) #pour eviter le clash des deux ForeignKey
    note=models.IntegerField()
    semaine=models.ForeignKey(Semaines,on_delete=models.CASCADE)

    