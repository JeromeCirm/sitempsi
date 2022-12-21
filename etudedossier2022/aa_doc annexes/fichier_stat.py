#
#     A revoir, chemins d'accès etc !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# 
# 
# import pandas as pd

annees=["2018","2019","2020","2021"]

donnees={ annee : pd.read_csv('Bureau/ProjectMenu/aa_doc annexes/lycees'+annee+'.csv',sep=";") for annee in annees}

## Extraits les colonnes intéressantes

list_colonnes_old={  'Presents - S' : "Presents", 'Taux de reussite - S' : "Reussite" , 'Taux de mentions - S' : "Mentions" }
list_colonnes={ 'Presents - Toutes series' : "Presents", 'Taux de reussite - Toutes series' : "Reussite" , 'Taux de mentions - Toutes series' : "Mentions"}

donnees_extraites={}
for annee in annees:
    if int(annee)<2021:
        colonnes=list_colonnes_old
    else:
        colonnes=list_colonnes
    donnees_extraites[annee]=donnees[annee][['UAI',*colonnes]].copy()
    nom_colonnes={ x : colonnes[x]+annee for x in colonnes}
    donnees_extraites[annee].rename(columns=nom_colonnes,inplace=True)


## Harmonise les UAI manquants

for x in annees:
    col=['UAI',*[label+x for label in colonnes.values()]]
    print(col)
    for y in annees:
        if x!=y:
            for uai in donnees_extraites[y]['UAI']:
                if not any(donnees_extraites[x]['UAI']==uai):
                    new_line=pd.DataFrame([[uai,None,None,None ]],columns=col)
                    donnees_extraites[x]=pd.concat([donnees_extraites[x],new_line], ignore_index=True)

## Fusionne en une seule table

resultat=None

for x in annees:
    if resultat is None:
        resultat=donnees_extraites[x]
    else:
        resultat=resultat.merge(donnees_extraites[x])

## Sauvegarde le resultat en csv

resultat.to_csv('Bureau/ProjectMenu/aa_doc annexes/lycees.csv',sep=";")

## test de lecture

fichier_lycee=pd.read_csv('Bureau/ProjectMenu/aa_doc annexes/lycees.csv',sep=";")
df_mask=fichier_lycee['UAI']=='0011119L'
res=fichier_lycee[df_mask]
index=res.iat[0,0]
valeurs={col : res.at[index,col] for col in res.columns}


