from sqlalchemy import create_engine
import pandas as pd
from os import remove,listdir,mkdir,path
from django.contrib.auth.models import Group, User
from .models import SauvegardeSelection2025
from json import dumps,loads,dump
import base64
import shutil
from etudedossier2024.models import AnciensEleves

engine=create_engine('sqlite:///etudedossier2025/stockage/versionxls.db',echo=False)
fichier_lycee=pd.read_csv('etudedossier2025/aa_doc annexes/lycees.csv',sep=";")

def p(s): # protection des noms de colonnes en SQL
    return '`'+s+'`'

lesfichiersPDF=listdir("etudedossier2025/fiches")
associationColonnes={
    "numeroDossier" : "numeroDossier",
    "nom" : "nom",
    "prenom" : "prenom",
    "sexe" : "sexe",
    "boursier" : "boursier",
    "dateNaissance" : "dateNaissance",
    "encf" : "ENCF",

    "lycee" : "lycee",
    "rneLycee" : "rneLycee",
    "ville" : "ville",
    "departement" : "departement",
    "entreeSeconde" : "entreeSeconde",
    "typeClasse" : "typeClasse",    # en term ou reorientation par exemple
    "nomClasse" : "nomClasse",   
    "edsTerm1" : "edsTerm1",
    "edsTerm2" : "edsTerm2",
    "eds1ere" : "eds1ere",
    "noteMath1ere" : "noteMath1ere",
    "notePhysique1ere" : "notePhys1ere",

    "noteautoScience" : "noteautoScience",
    "noteautoLettre" : "noteautoLettre",
    "noteautoMoyenne" : "notemoyenneSLettres",     # nouveau à gérer
    "noteautoGlobale" : "noteautoInitiale",
    "categorieDossier" : "categorieDossier",

    "niveauClasse" : "niveauClasse",
    "avisProviseur" : "avisProviseur",
    "avisProviseurDetail" : "avisProviseurDetail",   # nouveau  à gérer
    "methodeTravail" : "methodeTravail",
    "autonomie" : "autonomie",
    "capaciteInvestir" : "capaciteInvestir",
    "autresElements" : "autresElements",
    "lettreMotivation" : "lettreMotivation",    # nouveau à vérifier

    "noteActuelle" : "noteActuelle",
    "commentaireTraitement" : "commentaireTraitement",

    "motclebon" : "motclebon",
    "motclemauvais" : "motclemauvais",
    "dossierEtudie" : "dossierEtudie",
    "arevoir" : "arevoir",
    "dossierRisque" : "dossierRisque",
    "specialVire" : "specialVire",
    "problemeRepere" : "problemeRepere",
    "persoMarc" : "persoMarc",
    "rangalafin" : "rangalafin",
    "binome" : "binome",   # à modifier 
    "sauvegarde" : "sauvegarde",  # ajout à la fin
    "rangfinphase" : "rangfinphase",
    "rangfinal" : "rangfinal",

    "noteBacMath" : "noteBacMath",
    "noteBacPhys" : "noteBacPhys",
    "noteBacNSI" : "noteBacNSI",
    "noteBacSI" : "noteBacSI",

    "noteMathTerm" : "noteMathTerm",
    "rangMathTerme" : "rangMathTerme",
    "effectifMathTerm" : "effectifMathTerm",
    "noteMathExpertes" : "noteMathExpertes",
    "rangMathExpertes" : "rangMathExpertes",
    "effectifMathExpertes" : "effectifMathExpertes",
    "notePhysiqueTerm" : "notePhysiqueTerm",
    "rangPhysiqueTerm" : "rangPhysiqueTerm",
    "effectifPhysiqueTerm" : "effectifPhysiqueTerm",
    "noteLV1" : "noteLV1",
    "rangLV1" : "rangLV1",
    "effectifLV1" : "effectifLV1",
    "notePhilo" : "notePhilo",
    "rangPhilo" : "rangPhilo",
    "effectifPhilo" : "effectifPhilo",
    "bacFrEcrit" : "bacFrEcrit",
    "bacFrOral" : "bacFrOral",
    "noteSIPhysique" : "noteSIPhysique",
    "rangSIPhysique" : "rangSIPhysique",
    "effectifSIPhysique" : "effectifSIPhysique",
    "noteNSI" : "noteNSI",
    "rangNSI" : "rangNSI",
    "effectifNSI" : "effectifNSI",
    "noteMathComplementaires" : "noteMathComplementaires",
    "rangMathComplementaires" : "rangMathComplementaires",
    "effectifMathComplementaires" : "effectifMathComplementaires",

    "NBmotmauvais" : "NBmotmauvais", # nombre de mots-clefs en rouge
}

associationColonnesLycees= {
    "rne" : "Colonne5",
    "nom" : "Colonne5",
    "ville" : "Colonne5",
    "departement" : "Colonne5",
    "pourcentBac" : "Colonne5",
    "pourcentMention" : "Colonne5",
    "diffMath" : "Colonne5",
    "diffPhys" : "Colonne5",
}

categorie_dic= {
    "tresBon" : 700,
    "bon" : 1000,
    "moyenPlus" : 1250,
    "moyenMoins" : 1500,
    "aLaRigueur" : 1750,
    "pasBon" : 2000,
}

categorieText_dic= {
    "tresBon" : "très bon",
    "bon" : "bon",
    "moyenPlus" : "moyen plus",
    "moyenMoins" : "moyen moins",
    "aLaRigueur" : "à la rigueur",
    "pasBon" : "pas bon",
    "surtoutPas" : "surtout pas"
}

couleurs_dic={
    "tresBon" : "#008000",
    "bon" : "#207000",
    "moyenPlus" : "#407000",
    "moyenMoins" : "#705000",
    "aLaRigueur" : "#703000",
    "pasBon" : "#701000",
    "surtoutPas" : "#800000"
}

associe_binome_dic = {
    "B1" : "Catherine - Jérôme",
    "B2" : "Pierre B - Marc",
    "B3" : "Florent - Pierre C",
    "B4" : "Frédéric - Tommy"
}

listechoix={ # liste des items de tris dans sélection
        "le nom" : associationColonnes["nom"],
        "le prénom" : associationColonnes["prenom"],
        "le numéro de dossier" : associationColonnes["numeroDossier"],
        "le RNE du lycée" : associationColonnes["rneLycee"],
        "le lycée" : associationColonnes["lycee"],
        "la ville" : associationColonnes["ville"],
        "le département" : associationColonnes["departement"],
        "la note actuelle" : associationColonnes["noteActuelle"],
        "la note initiale" : associationColonnes["noteautoGlobale"],
        "le niveau de la classe" : associationColonnes["niveauClasse"],
        "l'avis du proviseur" : associationColonnes["avisProviseur"],
        "le nom de la classe" : associationColonnes["nomClasse"],
        "le binôme" : associationColonnes["binome"],
        "le rang en phase principale" : associationColonnes["rangfinphase"],
        "le nombre de mots-clefs en rouge" : associationColonnes["NBmotmauvais"],
}

def couleur(txt):
    if (txt=="très bon") : return "#008000" 
    if (txt=="bon") : return "#207000"    
    if (txt=="moyen plus") : return "#407000"    
    if (txt=="moyen moins") : return "#705000"    
    if (txt=="à la rigueur") : return "#703000"    
    if (txt=="pas bon") : return "#701000"    
    if (txt=="surtout pas") : return "#800000"    

def prepare_selection(context,request):
    def recupere_selection(utilise_sauvegarde=True):
        champs={
            "nom" : associationColonnes["nom"],
            "prénom" : associationColonnes["prenom"],
            "numéro de dossier" : associationColonnes["numeroDossier"],
            "RNE du lycée" : associationColonnes["rneLycee"],
            "nom du lycée" : associationColonnes["lycee"],
            "ville" : associationColonnes["ville"],
            "département" : associationColonnes["departement"],
            "note actuelle" : associationColonnes["noteActuelle"],
            "niveau de la classe" : associationColonnes["niveauClasse"],
            "avis du proviseur" : associationColonnes["avisProviseur"],
            "nom de la classe" : associationColonnes["nomClasse"],
            "binôme" : associationColonnes["binome"],
            "dossier étudié(oui/non)" : associationColonnes["dossierEtudie"],
            "dossier à revoir(oui/non)" : associationColonnes["arevoir"],
            "A revoir ensemble(oui/non)" : associationColonnes["dossierRisque"],
            "etiquette" : associationColonnes["categorieDossier"],
        }        
        if utilise_sauvegarde:
            try:
                obj=SauvegardeSelection2025.objects.get(user=request.user)
                if obj.pasexpert:
                    context["pasexpert"]="oui"
                else:
                    context["pasexpert"]="non"
                if obj.boursier:
                    context["boursier"]="oui"
                else:
                    context["boursier"]="non"
                ordre=loads(obj.ordre)
                ordreliste=[]
                for x in ordre:
                    x=int(x)
                    if x<0:
                        ordreliste.append([-x-1,1])
                    else:
                        ordreliste.append([x,0])
                context["ordre"]=ordreliste
                valeurs=loads(obj.valeur)
                i=0
                newchamps={}
                for x in champs:
                    newchamps[x]=(champs[x],valeurs[i])
                    i+=1 
                context["champs"]=newchamps       
                return
            except:
                pass
        context["pasexpert"]="non"
        context["boursier"]="non"
        context["ordre"]=[]
        newchamps={}
        for x in champs:
               newchamps[x]=(champs[x],"")
        context["champs"]=newchamps
    if request.method=="POST":
        if "choixAction" in request.POST:
            if request.POST["choixAction"]=="sauvegarde":
                try:
                    obj=SauvegardeSelection2025.objects.get(user=request.user)
                except:
                    obj=SauvegardeSelection2025(user=request.user)
                obj.valeur=dumps(dict(request.POST)["valeur[]"])
                if "ordre[]" in request.POST:
                    obj.ordre=dumps(dict(request.POST)["ordre[]"])
                else:
                     obj.ordre=dumps([])
                if "pasexpert" in request.POST:
                    obj.pasexpert=True
                else:
                    obj.pasexpert=False
                if "boursier" in request.POST:
                    obj.boursier=True
                else:
                    obj.boursier=False
                obj.save()
                recupere_selection()
            elif request.POST["choixAction"]=="efface":
                recupere_selection(False)
            elif request.POST["choixAction"]=="charge":
                recupere_selection()
    else:
        recupere_selection()
    context["listechoix"]=listechoix
    context["binome"]=associe_binome_dic
    context["pile"]=dumps([])
    context["indicePile"]=0
    context["etiquettes"]=categorieText_dic

def creation_requete(request,context):
    def echap(s):
        res='"'+s+'"'
        return res
    def text(x):
        for z in listechoix:
            if x==0:
                return listechoix[z]
            x-=1
    selection=""
    orderby=""
    if request.method=='POST':  
        try: # récupération de la condition ORDER BY
            context["orderby"]=request.POST.getlist('ordre[]')
            deja_une_condition=False
            orderby=""
            for x in request.POST.getlist('ordre[]'):
                x=int(x)
                if deja_une_condition: orderby+=","
                else: 
                    orderby=" ORDER BY "
                    deja_une_condition=True
                if int(x)<0:
                    x=-x-1
                    orderby+=text(x)
                    orderby+=" DESC"
                else:
                    orderby+=text(x)
        except:
            #print("pas de condition ORDER BY")
            orderby=""
        try : # récupération de la sélection
            selection=""
            deja_une_condition=False
            if "pasexpert" in request.POST:
                context["pasexpert"]=True
                deja_une_condition=True
                selection=" WHERE ("+p(associationColonnes["noteMathExpertes"])+" IS NULL OR "+p(associationColonnes["notePhysiqueTerm"])+" IS NULL)"
            if "boursier" in request.POST:
                context["boursier"]=True
                if deja_une_condition: selection+=" AND "
                else:
                    selection=" WHERE "
                    deja_une_condition=True
                selection+=p(associationColonnes["boursier"])+"!='Non boursier'"
            nomcolonne=request.POST.getlist('nomcolonne[]')
            valeurcolonne=request.POST.getlist('valeur[]')
            context["nomcolonne"]=nomcolonne
            context["valeurcolonne"]=valeurcolonne
            for i in range(len(valeurcolonne)):
                if valeurcolonne[i]!="":
                    if deja_une_condition: selection+=" AND "
                    else:
                        selection=" WHERE "
                        deja_une_condition=True
                    selection+=p(nomcolonne[i])+"="+echap(valeurcolonne[i])
        except:
            print("erreur dans le select")
            selection=""
    return selection+orderby

def trouve_rang(liste,note): # trouve le rang dans la liste décroissante
    try:
        note=float(note)
    except:
        return len(liste)-1
    deb,fin=0,len(liste)-1
    while deb<fin:
        mid=(deb+fin)//2
        if liste[mid]==note: return mid+1
        if liste[mid]<note: fin=mid
        else: deb=mid+1
    return mid+1


def lire_tous_les_dossiers(request,context):
    fin_requete=creation_requete(request,context)
    lesnotes=recuperer_les_notes()
    i=0
    with engine.connect() as conn :
        res=conn.execute("SELECT * FROM parcoursup "+fin_requete).fetchall()
        lesdossiers=[]
        for row in res:
            i+=1
            un_dossier={}
            for x in associationColonnes:
                un_dossier[x]=row[associationColonnes[x]]
            un_dossier["compteur"]=i
            un_dossier["rangActuel"]=trouve_rang(lesnotes,un_dossier["noteActuelle"])
            lesdossiers.append(un_dossier)
        context["lesdossiers"]=lesdossiers

def nb_boursier(limite=1500):
    with engine.connect() as conn :
        cmd="SELECT count(*) FROM (SELECT * FROM parcoursup ORDER BY "+p(associationColonnes["noteActuelle"])+" DESC LIMIT "+str(limite)+") WHERE "+p(associationColonnes["boursier"])+"!='Non boursier'"
        #print(cmd)
        res=conn.execute(cmd).fetchall()
        #print(res[0][0])
        return (res[0][0])
 
def lire_stat(rne):
    def f(x):
        try:
            return int(x)
        except:
            return ""
    try:
        df_mask=fichier_lycee['UAI']==rne
        res=fichier_lycee[df_mask]
        index=res.iat[0,0]
        return {col : f(res.at[index,col]) for col in res.columns}
    except:
        return {}

def lire_un_dossier(request,context):
    def nom_fichier_pdf():
        numdossier="-"+str(dossier[associationColonnes["numeroDossier"]])+"-"
        for x in lesfichiersPDF:
            if numdossier in x:
                return base64.b32encode(bytes(x,"utf-8"))
        return base64.b32encode(bytes("","utf-8"))
        #nom=dossier[associationColonnes["nom"]].replace(" ","").replace("'","")
        #return "dossiers_0750660K_MPSI-"+str(dossier[associationColonnes["numeroDossier"]])+"-"+nom+".pdf"
    def nb_dossiers_lycee():
        res=conn.execute("SELECT COUNT(*) FROM parcoursup WHERE `"+associationColonnes["rneLycee"]+"`=\""+str(dossier[associationColonnes["rneLycee"]])+"\"").fetchall()
        return res[0][0]
    fin_requete=creation_requete(request,context)
    ligne=1
    try:
            ligne=int(request.POST.get('NumeroLigne'))
            if ligne<1: ligne=1
    except:
            #print("POST[NumeroLigne] non définie")
            pass
    with engine.connect() as conn :
        res=conn.execute("SELECT * FROM parcoursup "+fin_requete).fetchall()
        if ligne>len(res): return False  # pas assez de ligne
        row=res[ligne-1]  # une seule ligne normalement
        dossier={}
        for x in associationColonnes:
            try:
                dossier[x]=row[associationColonnes[x]]
            except:
                print(associationColonnes[x]," non trouvée")
        context["dossier"]=dossier
        context["categorie"]=categorie_dic
        context["couleurs"]=couleurs_dic
        context["couleurCategorie"]=couleur(dossier["categorieDossier"])
        context["binome"]=associe_binome_dic.get(dossier["binome"],"Tout le monde")
        context["maxligne"]=len(res)
        context["ligne"]=ligne
        context["lesnotes"]=recuperer_les_notes()
        context["tauxBoursier"]=int(nb_boursier(1500)/1.5)/10
        context["tauxBoursier1750"]=int(nb_boursier(1750)/1.75)/10
        context["tauxBoursier2000"]=int(nb_boursier(2000)/2)/10
        context["statslycee"]=lire_stat(dossier[associationColonnes["rneLycee"]])
        context["nompdf"]=nom_fichier_pdf()
        context["dossierLycée"]=nb_dossiers_lycee()
        rg,offset,notes_offset=calcul_rang_final(row)
        context["rangfinalestime"]=rg
        context["offset"]=offset
        context["notes_offset"]=notes_offset
        context["anciens_eleves"]=recup_anciens(dossier["rneLycee"])
        context["nb_anciens_eleves"]=len(context["anciens_eleves"])
        return True

def recuperer_les_notes(cate=""):
    with engine.connect() as conn :
        cmd="SELECT "+p(associationColonnes["noteActuelle"])+" FROM parcoursup "
        if cate!="":
            cmd+="WHERE "+p(associationColonnes["categorieDossier"])+"='"+cate+"'"
        res=conn.execute(cmd).fetchall()
        l=[]
        for x in res:
            try:
                val=float(x[associationColonnes["noteActuelle"]])
                if val==val:                   
                    l.append(val)
            except:
                pass
        return sorted(l,key=lambda x : -x)

def convertion_excel():
    global engine
    try:
        remove('etudedossier2025/stockage/versionxls.db')
    except:
        pass
    df=pd.read_excel('etudedossier2025/stockage/fichierinitial.xlsx')
    # pour modifier les colonnes passées en float avec valeurs nan par Marc
    # commentaireTraitement est maintenant directement mis par Marc
    liste={"arevoir" : str, "dossierEtudie" : str, "dossierRisque" : str}
    df=df.astype({associationColonnes[x] : str for x in liste})
    df=df.assign(**{associationColonnes[x] : "" if x=="commentaireTraitement" else "non" for x in liste})
    ## *5 des notes auto
    def fois_5(x):
        try:
            return int(5*x*1000)/1000
        except:
            return 0
    liste={ "noteautoScience","noteautoLettre","noteautoMoyenne","noteautoGlobale"}
    for col in liste:
        nom_col=associationColonnes[col]
        df[nom_col]=df[nom_col].apply(fois_5)
    ## gérer la nouvelle note initiale
    df[associationColonnes["noteActuelle"]]=df[associationColonnes["noteautoGlobale"]]
    ## mettre les nouvelles colonnes:
    df[associationColonnes["sauvegarde"]]=""
    df[associationColonnes["rangfinphase"]]=""
    df[associationColonnes["rangfinal"]]=""
    ## gérer les "mauvais lycées"
    col_note=associationColonnes["noteActuelle"]
    col_cate=associationColonnes["categorieDossier"]
    les_notes=sorted(df[col_note].to_list(),key=lambda x : -x)
    def min_mention(uai):
        #renvoie False uniquement si >40 les deux années 2018 et 2019
        try:    
            df_mask=fichier_lycee['UAI']==uai
            res=fichier_lycee[df_mask]
            index=res.iat[0,0]
            if res.at[index,"Mentions2018"]<40: 
                return True
            if res.at[index,"Mentions2019"]<40: 
                return True
            return False
        except:
            return True
    # la partie qui suit est annulée : c'est MArc qui gère les lycées avec faible taux de mention/réussite 
    # complètement
    if False:
        for index, row in df.iterrows():
            rang=trouve_rang(les_notes,row[col_note])
            if min_mention(row[associationColonnes['rneLycee']]):
                if rang>categorie_dic["pasBon"]:
                    df.at[index,col_cate]="surtout pas"
                elif rang>categorie_dic["aLaRigueur"]:
                    df.at[index,col_cate]="pas bon"
                else:
                    df.at[index,col_cate]="à la rigueur"
    ## gèreles commentaire none/nan
    col_comm=associationColonnes['commentaireTraitement']
    df=df.astype({col_comm : str})
    for index, row in df.iterrows():
        if row[col_comm] in ["nan","None"]:
            df.at[index,col_comm]=""
    ## gérer les colonnes qui devraient être entière et qui ne le sont pas
    def convert_int(x,default=0):
        try:
            return int(x)
        except:
            return default
    liste={"entreeSeconde","departement","rangMathTerme","effectifMathTerm",
    "rangMathExpertes","effectifMathExpertes","rangPhysiqueTerm","effectifPhysiqueTerm",
    "rangLV1","effectifLV1","rangPhilo","effectifPhilo","rangSIPhysique","effectifSIPhysique",
    "rangNSI","effectifNSI","rangMathComplementaires","effectifMathComplementaires"}
    for x in liste:
        df[x]=df[x].apply(convert_int)
    df=df.astype({associationColonnes[x] : int for x in liste})
    engine = create_engine('sqlite:///etudedossier2025/stockage/versionxls.db', echo=False)
    df.to_sql('parcoursup', con=engine)
    ## remise à zéro des sélections de chacun
    gretudedossier=Group.objects.get(name="etudedossier")
    for prof in gretudedossier.user_set.all():
        obj,created=SauvegardeSelection2025.objects.update_or_create(user=prof)
        obj.valeur=dumps([])
        obj.ordre=dumps([])
        #obj.boursier=False
        #obj.pasexpert=False
        obj.save()


def eng(str): # échapper les guillements
    return  str.replace('"',"'")

def est_encf(num_dossier):
    # renvoie vrai si le dossier est ENCF ou en cas d'erreur
    try:
        with engine.connect() as conn :
            res=conn.execute("SELECT * FROM parcoursup WHERE "+p(associationColonnes["numeroDossier"])+"='"+str(num_dossier)+"'").fetchall()
            if len(res)!=1:
                return True
            row=res[0] # une seule ligne normalement
            return row[associationColonnes["encf"]]=="ENCF"
    except:
        return True

def maj_dossier(request):
    with engine.connect() as conn :
        if est_encf(request.POST['NumeroDossier']):  # patch pour ne pas modifier les ENCF 
            return
        if "arevoir" in request.POST: arevoir="oui"
        else : arevoir="non"
        if "risque" in request.POST: risque="oui"
        else : risque="non"
        cmd="UPDATE parcoursup SET "+p(associationColonnes["noteActuelle"])+"='"+request.POST["NouvelleNote"]+"'"
        cmd+=","+p(associationColonnes["commentaireTraitement"])+"=\""+eng(request.POST["Commentaire"])+"\""
        cmd+=","+p(associationColonnes["arevoir"])+"='"+arevoir+"'"
        cmd+=","+p(associationColonnes["dossierRisque"])+"='"+risque+"'"
        cmd+=","+p(associationColonnes["dossierEtudie"])+"='oui'"
        cmd+=","+p(associationColonnes["categorieDossier"])+"='"+request.POST["CategorieDossier"]+"'"
        cmd+=" WHERE "+p(associationColonnes["numeroDossier"])+"='"+request.POST['NumeroDossier']+"'"
        #print(cmd)
        conn.execute(cmd)

def convertion_xslx():
    engine = create_engine('sqlite:///etudedossier2025/stockage/versionxls.db', echo=False)
    with engine.connect() as conn:
        df=pd.read_sql("SELECT * FROM parcoursup",conn)
    df.to_excel('etudedossier2025/stockage/fichierfinal.xlsx',sheet_name='parcoursup')    

def sauvegarde_phase_generale():
    with engine.connect() as conn :
        try:
            cmd='ALTER TABLE parcoursup ADD sauvegarde VARCHAR(100)'
            conn.execute(cmd)
        except:
            pass
        lesnotes=recuperer_les_notes()
        res=conn.execute("SELECT * FROM parcoursup ").fetchall()
        for row in res:
            cmd='UPDATE parcoursup SET sauvegarde="'+str(trouve_rang(lesnotes,row[associationColonnes["noteActuelle"]]))+' ('+row[associationColonnes["categorieDossier"]]+')"'
            cmd+=" WHERE "+p(associationColonnes["numeroDossier"])+"='"+str(row[associationColonnes['numeroDossier']])+"'"
            conn.execute(cmd)

def calcul_rang_final(row):
        lesnotes={}
        lesnotes["très bon"]=recuperer_les_notes("très bon")
        lesnotes["bon"]=recuperer_les_notes("bon")
        lesnotes["moyen plus"]=recuperer_les_notes("moyen plus")
        lesnotes["moyen moins"]=recuperer_les_notes("moyen moins")
        lesnotes["à la rigueur"]=recuperer_les_notes("à la rigueur")
        lesnotes["pas bon"]=recuperer_les_notes("pas bon")
        lesnotes["surtout pas"]=recuperer_les_notes("surtout pas")
        offset={}
        notes_offset={}
        offset["très bon"]=0,lesnotes["très bon"][0]
        notes_offset["très bon"]=lesnotes["très bon"][0]
        offset["bon"]=offset["très bon"][0]+len(lesnotes["très bon"]),lesnotes["bon"][0]
        notes_offset["bon"]=lesnotes["bon"][0]
        offset["moyen plus"]=offset["bon"][0]+len(lesnotes["bon"]),lesnotes["moyen plus"][0]
        notes_offset["moyen plus"]=lesnotes["moyen plus"][0]
        offset["moyen moins"]=offset["moyen plus"][0]+len(lesnotes["moyen plus"]),lesnotes["moyen moins"][0]
        notes_offset["moyen moins"]=lesnotes["moyen moins"][0]
        offset["à la rigueur"]=offset["moyen moins"][0]+len(lesnotes["moyen moins"]),lesnotes["à la rigueur"][0]
        notes_offset["à la rigueur"]=lesnotes["à la rigueur"][0]
        offset["pas bon"]=offset["à la rigueur"][0]+len(lesnotes["à la rigueur"]),lesnotes["pas bon"][0]
        notes_offset["pas bon"]=lesnotes["pas bon"][0]
        offset["surtout pas"]=offset["pas bon"][0]+len(lesnotes["pas bon"]),lesnotes["surtout pas"][0]
        notes_offset["surtout pas"]=lesnotes["surtout pas"][0]
        note=row[associationColonnes["noteActuelle"]]
        cate=row[associationColonnes["categorieDossier"]]
        rg=trouve_rang(lesnotes[cate],note)+offset[cate][0]
        return rg,offset,0
        

def rang_fin_phase():
    # ajuste les classements en priorisant les catégories
    # sauvegarder avant de faire cela ! (ligne au dessus dans gestion)
    with engine.connect() as conn :
        try:
            cmd='ALTER TABLE parcoursup ADD rangfinphase INTEGER'
            conn.execute(cmd)
        except:
            pass
        lesnotes={}
        lesnotes["très bon"]=recuperer_les_notes("très bon")
        lesnotes["bon"]=recuperer_les_notes("bon")
        lesnotes["moyen plus"]=recuperer_les_notes("moyen plus")
        lesnotes["moyen moins"]=recuperer_les_notes("moyen moins")
        lesnotes["à la rigueur"]=recuperer_les_notes("à la rigueur")
        lesnotes["pas bon"]=recuperer_les_notes("pas bon")
        lesnotes["surtout pas"]=recuperer_les_notes("surtout pas")
        res=conn.execute("SELECT * FROM parcoursup ").fetchall()
        offset={}
        offset["très bon"]=0
        offset["bon"]=offset["très bon"]+len(lesnotes["très bon"])
        offset["moyen plus"]=offset["bon"]+len(lesnotes["bon"])
        offset["moyen moins"]=offset["moyen plus"]+len(lesnotes["moyen plus"])
        offset["à la rigueur"]=offset["moyen moins"]+len(lesnotes["moyen moins"])
        offset["pas bon"]=offset["à la rigueur"]+len(lesnotes["à la rigueur"])
        offset["surtout pas"]=offset["pas bon"]+len(lesnotes["pas bon"])
        def rang(row) :
            note=row[associationColonnes["noteActuelle"]]
            cate=row[associationColonnes["categorieDossier"]]
            rg=trouve_rang(lesnotes[cate],note)+offset[cate]
            return str(rg)       
        for row in res:
            cmd='UPDATE parcoursup SET rangfinphase='+rang(row)
            cmd+=" WHERE "+p(associationColonnes["numeroDossier"])+"='"+str(row[associationColonnes['numeroDossier']])+"'"
            #print(cmd)
            #break
            conn.execute(cmd)   

def rang_final():
    with engine.connect() as conn :
        try:
            cmd='ALTER TABLE parcoursup ADD rangfinal INTEGER'
            conn.execute(cmd)
        except:
            pass
        try:
            cmd='ALTER TABLE parcoursup MODIFY rangfinal INTEGER'
            conn.execute(cmd)
        except:
            pass        
        cates=["très bon","bon","moyen plus","moyen moins","à la rigueur","pas bon","surtout pas"]
        rang=0
        encf=0
        for cate in cates:
            cmd="SELECT * FROM parcoursup WHERE "+p(associationColonnes["categorieDossier"])+"='"+cate+"' ORDER BY "+p(associationColonnes["noteActuelle"])+" DESC"
            res=conn.execute(cmd).fetchall()        
            for row in res:
                if row[associationColonnes['encf']]=='ECF':
                    rang+=1
                    cmd="UPDATE parcoursup SET rangfinal="+str(rang)+" WHERE "+p(associationColonnes["numeroDossier"])+"='"+str(row[associationColonnes['numeroDossier']])+"'"
                    conn.execute(cmd)  
                    #print(cmd)
                    #print(1/0)
                else:
                    encf+=1
                    cmd="UPDATE parcoursup SET rangfinal=5000 WHERE "+p(associationColonnes["numeroDossier"])+"='"+str(row[associationColonnes['numeroDossier']])+"'"
                    conn.execute(cmd)                    
            #print(cate,rang,encf) 


def patch_old1():
    # récupération des betises car Zoé et Catherine ont commencé en avance!
    with engine.connect() as conn:
        for txt in ["dossierRisque","dossierEtudie","arevoir"]:
            conn.execute('UPDATE parcoursup SET '+p(associationColonnes[txt])+'="non" WHERE '+p(associationColonnes[txt])+'!="oui"')
            conn.execute('UPDATE parcoursup SET '+p(associationColonnes[txt])+'="non" WHERE '+p(associationColonnes[txt])+' IS NULL')

def patch_old2():
    # mise à jour des colonnes motclemauvais et problemeRepere en cours de route !
    df_new=pd.read_excel('etudedossier3/stockage/fichierinitial.xlsx')
    engine = create_engine('sqlite:///etudedossier2025/stockage/versionxls.db', echo=False)
    with engine.connect() as conn:
        for index, row in df_new.iterrows():
            cmd="UPDATE parcoursup SET "+associationColonnes["motclemauvais"]+"=\""+eng(str(row[associationColonnes['motclemauvais']]))
            cmd+="\","+associationColonnes["problemeRepere"]+"=\""+eng(str(row[associationColonnes["problemeRepere"]]))
            cmd+="\" WHERE "+associationColonnes["numeroDossier"]+"="+eng(str(row[associationColonnes["numeroDossier"]]))
            #print(cmd)
            #break
            conn.execute(cmd)

def patch_old3():
    # rajout de la colonne encf en cours de traitement
    df_new=pd.read_excel('etudedossier2025/stockage/fichierinitial.xlsx')
    engine = create_engine('sqlite:///etudedossier2025/stockage/versionxls.db', echo=False)
    with engine.connect() as conn:
        conn.execute("ALTER TABLE parcoursup ADD encf VARCHAR(30)")
        for index, row in df_new.iterrows():
            cmd="UPDATE parcoursup SET encf=\""+row['ENCF']+"\" WHERE numeroDossier=\"" +str(row['numeroDossier'])+"\""
            #print(cmd)
            #break
            conn.execute(cmd)  

def patch():
    pass    

def test_jerome():
    def fgint(x):
        try:
            return int(x)
        except:
            return 8000
    engine = create_engine('sqlite:///etudedossier2025/stockage/versionxls.db', echo=False)
    with engine.connect() as conn:
        df=pd.read_sql("SELECT * FROM parcoursup",conn)
        c=associationColonnes["rangfinal"]
        df["rangjerome"]=8000
        for index, row in df.iterrows():
            df.at[index,"rangjerome"]=int(df.at[index,c])
        df.to_excel('etudedossier2025/stockage/fichierfinal.xlsx',sheet_name='parcoursup')    
        #print(df.dtypes)
        return
        if False:
            print(df.at[index,c],type(df.at[index,c]),int(df.at[index,c]),type(int(df.at[index,c])))
            return
        df.astype({associationColonnes["rangfinal"]:"int",associationColonnes["numeroDossier"]:"int"})
        df["rangjerome"]=fgint(df[associationColonnes["rangfinal"]])
        df.to_excel('etudedossier2025/stockage/fichierfinal.xlsx',sheet_name='parcoursup')    
        if False:
            rang=trouve_rang(les_notes,row[col_note])
            if min_mention(row[associationColonnes['rneLycee']]):
                if rang>categorie_dic["pasBon"]:
                    df.at[index,col_cate]="surtout pas"
                elif rang>categorie_dic["aLaRigueur"]:
                    df.at[index,col_cate]="pas bon"
                else:
                    df.at[index,col_cate]="à la rigueur"

def convertion_xslx_minimal():
    with engine.connect() as conn:
        df=pd.read_sql("SELECT * FROM parcoursup",conn)
        c=associationColonnes["rangfinal"]
        df["classement"]=""
        df["testjerome"]=8000
        for index, row in df.iterrows():
            if df.at[index,associationColonnes["encf"]]=="ENCF":
                df.at[index,"classement"]="ENCF"
            else:
                rg=int(df.at[index,c])
                if rg>3000:
                    df.at[index,"classement"]="NC"
                else:
                    df.at[index,"classement"]=str(rg)
                df.at[index,"testjerome"]=rg
        df.to_excel('etudedossier2025/stockage/fichierfinal.xlsx',sheet_name='parcoursup')    

def extraction_donnees(request):
    context={}
    login=request.POST["extraction_donnees_login"]
    try:
        lire_un_dossier(request,context)
        donnees_a_extraire={}
        donnees_a_extraire["prenomofficiel"]=context["dossier"]["prenom"]
        donnees_a_extraire["nomofficiel"]=context["dossier"]["nom"]
        donnees_a_extraire["rne_lycee"]=context["dossier"]["rneLycee"]
        donnees_a_extraire["note_initiale"]=context["dossier"]["noteautoGlobale"]
        donnees_a_extraire["note_finale"]=context["dossier"]["noteActuelle"]
        donnees_a_extraire["lycee_officiel"]=context["dossier"]["lycee"]
        donnees_a_extraire["ville_officiel"]=context["dossier"]["ville"]
        donnees_a_extraire["departement_officiel"]=context["dossier"]["departement"]
        donnees_a_extraire["date_naissance_officiel"]=context["dossier"]["dateNaissance"] 
        donnees_a_extraire["numero_dossier_parcoursup"]=context["dossier"]["numeroDossier"]
        lesnotes=recuperer_les_notes()
        donnees_a_extraire["rang"]=trouve_rang(lesnotes,context["dossier"]["noteActuelle"])
        donnees_a_extraire["modif_auto"]=context["dossier"]["problemeRepere"]
        numdossier=str(context["dossier"]["numeroDossier"])
        if not path.exists("private_files/transfert_fiche"):
            mkdir("private_files/transfert_fiche")
        f = open("private_files/transfert_fiche/"+login+"_2025json", "w")
        dump(donnees_a_extraire,f)
        f.close()
        for x in lesfichiersPDF:
            if numdossier in x:
                shutil.copy("etudedossier2025/fiches/"+x,"private_files/transfert_fiche/"+login+"_2025.pdf")
        return "extraction réussie pour "+login
    except:
        return "extraction impossible pour "+login

def extraction_donnees(request):
    context={}
    commentaire=request.POST["extraction_donnees_login"]
    try:
        lire_un_dossier(request,context)
        num_dossier=context["dossier"]["numeroDossier"]
        prenom=context["dossier"]["prenom"]
        nom=context["dossier"]["nom"]
        rne=context["dossier"]["rneLycee"]
        note_initiale=context["dossier"]["noteautoGlobale"]
        note_finale=context["dossier"]["noteActuelle"]
        lesnotes=recuperer_les_notes()
        rang=trouve_rang(lesnotes,context["dossier"]["noteActuelle"])
        modif_auto=context["dossier"]["problemeRepere"]
        numdossier=str(context["dossier"]["numeroDossier"])
        if request.user.username in ["nizon","bouissou"]:
            classe="MPSI1"
        elif request.user.username in ["connault","kopp"]:
            classe="MPSI2"
        else:
            classe=""
        try:
            obj=AnciensEleves.objects.get(annee=2025,num_dossier=num_dossier)
            obj.commentaire=commentaire
            obj.save()
        except:
            AnciensEleves(annee=2025,classe=classe,num_dossier=num_dossier,rne=rne,prenom=prenom,nom=nom,note_initiale=note_initiale,note_finale=note_finale,
        rang=rang,modif_auto=modif_auto,commentaire=commentaire).save()
        return "extraction réussie "
    except:
        return "extraction impossible"

def recup_anciens(rne):
    return AnciensEleves.objects.filter(rne=rne)