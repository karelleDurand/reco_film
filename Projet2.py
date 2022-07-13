#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import datetime as dt
#tabTitleCrew=pd.read_csv("OneDrive/Documents/Projet 2/Base de données/title.crew.tsv.gz",sep="\t",nrows=10,index_col="tconst")
#tabTitleEpisode=pd.read_csv("OneDrive/Documents/Projet 2/Base de données/title.episode.tsv.gz",sep="\t",nrows=10,index_col="tconst")


# 1. Import des tables

#     1.1 Table Akas 

# In[53]:


#Import de la table title.akas
#Remplacement des \N par Nan
#Filtrer sur les régions = 'FR' avec le chunk
iter_csv=pd.read_csv("C:/Users/karelle/OneDrive/Documents/Projet 2/Base de données/bds/title.akas.tsv.gz",sep="\t",
                     index_col="titleId",
                     na_values="\\N", 
                     keep_default_na=True,
                     usecols=['titleId','title','region'])
tabTitleAka = pd.concat([chunk[chunk['region'] == 'FR'] for chunk in iter_csv])
#Suppression de la colonne 'region'
tabTitleAka=tabTitleAka.drop(columns=['region']).reset_index()
tabTitleAka


#     1.2 Table NameBasics

# In[2]:


#Import de la table name.basics
#Remplacement des \N par Nan
NameBasics=pd.read_csv("C:/Users/karelle/OneDrive/Documents/Projet 2/Base de données/name.basics.tsv.gz",sep="\t",
                       na_values="\\N",
                       index_col="nconst",
                       usecols=["nconst","primaryName","birthYear","knownForTitles"],
                       chunksize=1000)
tabNameBasics = pd.concat([chunk for chunk in NameBasics])
#transforme la colonne knowForTitle en 6 colonnes pour chaque film
#tabNameBasics[['film1','film2','film3','film4','film5','film6']]=tabNameBasics.knownForTitles.str.split(",", expand=True)
#Suppression de la colonne knowForTitle
#tabNameBasics=tabNameBasics.drop(columns=['knownForTitles'])
tabNameBasics


#     1.3 Table TitleBasics

# In[4]:


#Import de la table titlebasics
#Remplacement des \N par Nan
#Filtrer sur titleType = 'movie' et sur isAdult = '0'
iter =pd.read_csv("C:/Users/karelle/OneDrive/Documents/Projet 2/Base de données/bds/title.basics.tsv.gz",sep="\t",
                           index_col="tconst",
                           na_values="\\N",
                           usecols=["tconst","titleType","primaryTitle","startYear","isAdult","runtimeMinutes","genres"],
                           low_memory=True,
                           chunksize=1000)
tabTitleBasics = pd.concat([chunk[(chunk['titleType'] == 'movie') | (chunk['isAdult'] == 0)] for chunk in iter])
#REmplace les NaN par 'Autres' dans la colonne 'genres
tabTitleBasics['genres']=tabTitleBasics['genres'].replace(np.nan,'Autres')
#Remplace les NaN par des 0 dans la colonne startYear
tabTitleBasics['startYear']=tabTitleBasics['startYear'].replace(np.nan,0)
#convertit la colonne startYear en integer
tabTitleBasics['startYear']=tabTitleBasics['startYear'].astype(int)
#Suppression des colonnes titleType et isAdult
tabTitleBasics=tabTitleBasics.drop(columns=['titleType','isAdult']).reset_index()
tabTitleBasics


#     1.4 Table TitlePrincipals

# In[7]:


#Import de la table title.principals
#Remplace les \N par des NaN
tabTitlePrincipal=pd.read_csv("C:/Users/karelle/OneDrive/Documents/Projet 2/Base de données/title.principals.tsv.gz",sep="\t",
                              na_values="\\N",
                              usecols=["tconst","nconst","category"],
                              index_col="tconst")
tabTitlePrincipal


# In[18]:


tabTitlePrincipal['category'].value_counts()


#     1.5 Table TitleRating

# In[56]:


#Import de la table title.ratings
#Remplace les \N par des NaN
tabTitleRating=pd.read_csv("C:/Users/karelle/OneDrive/Documents/Projet 2/Base de données/title.ratings.tsv.gz",sep="\t",na_values="\\N",engine='c',index_col="tconst",low_memory=True)
tabTitleRating


# In[3]:


#Jointure entre les tables des films et des votes
df_inner1 = tabTitleRating.merge(tabTitleBasics, how='inner', left_index=True, right_index=True)
#Répartition des votes selon les genres
df_inner1=df_inner1.pivot_table(index="genres",columns="averageRating",values="numVotes",aggfunc='mean').head(20)
#plt.bar(df_inner1['genres'],df_inner1['averageRating'])


# In[ ]:


#jointure entre les tables df_inner précédente et TitlePrincipal
df_inner2 = df_inner1.merge(tabTitlePrincipal, how='inner', left_index=True, right_index=True)


# In[48]:


tab1=tabTitleAka.loc[(tabTitleAka['title'].str.contains('Épisode #'))]
tabTitleAka.drop(index=tab1.index)


# 2. Graphique sur la base initiale

#     2.1 Proportion des langues

# In[ ]:


tabTitleAka

