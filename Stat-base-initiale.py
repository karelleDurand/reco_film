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

# In[2]:


#Import de la table title.akas
#Remplacement des \N par Nan
tabTitleAka=pd.read_csv("C:/Users/karelle/OneDrive/Documents/Projet 2/Base de données/bds/title.akas.tsv.gz",sep="\t",
                     index_col="titleId",
                     na_values="\\N", 
                     keep_default_na=True,
                     usecols=['titleId','title','region'])
tabTitleAka=tabTitleAka.reset_index()
tabTitleAka


#     1.2 Table NameBasics

# In[2]:


#Import de la table name.basics
#Remplacement des \N par Nan
NameBasics=pd.read_csv("C:/Users/karelle/OneDrive/Documents/Projet 2/Base de données/bds/name.basics.tsv.gz",sep="\t",
                       na_values="\\N",
                       index_col="nconst",
                       usecols=["nconst","primaryName","birthYear","primaryProfession","knownForTitles"],
                       chunksize=1000)
tabNameBasics = pd.concat([chunk for chunk in NameBasics])
#transforme la colonne knowForTitle en 6 colonnes pour chaque film
#tabNameBasics[['film1','film2','film3','film4','film5','film6']]=tabNameBasics.knownForTitles.str.split(",", expand=True)
#Suppression de la colonne knowForTitle
#tabNameBasics=tabNameBasics.drop(columns=['knownForTitles'])
tabNameBasics


#     1.3 Table TitleBasics

# In[3]:


#Import de la table titlebasics
#Remplacement des \N par Nan
#Filtrer sur titleType = 'movie' et sur isAdult = '0'
tabTitleBasics =pd.read_csv("C:/Users/karelle/OneDrive/Documents/Projet 2/Base de données/bds/title.basics.tsv.gz",sep="\t",
                           index_col="tconst",
                           na_values="\\N",
                           usecols=["tconst","titleType","primaryTitle","startYear","isAdult","runtimeMinutes","genres"],
                           low_memory=True)
#Remplace les NaN par 'Autres' dans la colonne 'genres
tabTitleBasics['genres']=tabTitleBasics['genres'].replace(np.nan,'Autres')
#Remplace les NaN par des 0 dans la colonne startYear
tabTitleBasics['startYear']=tabTitleBasics['startYear'].replace(np.nan,0)
#convertit la colonne startYear en integer
tabTitleBasics['startYear']=tabTitleBasics['startYear'].astype(int)
tabTitleBasics=tabTitleBasics.reset_index()
tabTitleBasics


#     1.4 Table TitlePrincipals

# In[4]:


#Import de la table title.principals
#Remplace les \N par des NaN
tabTitlePrincipal=pd.read_csv("C:/Users/karelle/OneDrive/Documents/Projet 2/Base de données/bds/title.principals.tsv.gz",sep="\t",
                              na_values="\\N",
                              usecols=["tconst","nconst","category"],
                              index_col="tconst").reset_index()
tabTitlePrincipal


# In[18]:


tabTitlePrincipal['category'].value_counts()


#     1.5 Table TitleRating

# In[6]:


#Import de la table title.ratings
#Remplace les \N par des NaN
tabTitleRating=pd.read_csv("C:/Users/karelle/OneDrive/Documents/Projet 2/Base de données/bds/title.ratings.tsv.gz",sep="\t",na_values="\\N",engine='c',index_col="tconst",low_memory=True)
tabTitleRating


# 2. Graphique sur la base initiale

#     2.1 Proportion des langues

# In[31]:


plt.figure(figsize = (15,10))
count = tabTitleAka.groupby('region')['titleId'].count().sort_values(ascending = False).head(10).reset_index()
sns.barplot(data = count, x = 'region', y = 'titleId', color = 'lightblue')
plt.title('Proportion des langues dans la base de données initiale')
plt.xlabel('Version des films')
plt.ylabel('Count')
#plt.savefig('ProportionLangues.png', dpi=300)
plt.show()


# In[32]:


count1 = tabTitleAka.groupby('region')['titleId'].count().sort_values(ascending = False).reset_index()
count1


# In[37]:


count1['percent'] = round((count1['titleId']/count1['titleId'].sum())*100,2)
count1.head(10)


#     2.2 Proportion des types de films

# In[42]:


plt.figure(figsize = (15,10))
count_movie = tabTitleBasics.groupby('titleType')['tconst'].count().sort_values(ascending = False).head(10).reset_index()
sns.barplot(data = count_movie, x = 'titleType', y = 'tconst', color = 'lightblue')
plt.title('Proportion des types dans la base de données initiale')
plt.xlabel('Types de films')
plt.ylabel('Count')
#plt.savefig('ProportionTypes.png', dpi=300)
plt.show()


# In[45]:


count_movie1 = tabTitleBasics.groupby('titleType')['tconst'].count().sort_values(ascending = False).reset_index()
count_movie1


# In[47]:


count_movie1['percent'] = round((count_movie1['tconst']/count_movie1['tconst'].sum())*100,2)
count_movie1.head(10)


#     2.3 Proportion des genres

# In[4]:


#Split des genres avec un getdumies
tabGenre = tabTitleBasics['genres'].str.get_dummies(sep=',').dropna()
tabGenre


# In[9]:


genre = pd.DataFrame(tabGenre.sum().sort_values(ascending = False)).reset_index()
genre


# In[12]:


plt.figure(figsize = (15,10))
sns.barplot(data = genre, x = 'index', y = 0, color = 'lightblue')
plt.title('Proportion des genres dans la base de données initiale')
plt.xlabel('Genre des films')
plt.ylabel('Count')
plt.xticks(rotation = 90)
#plt.savefig('ProportionGenres.png', dpi=300)
plt.show()


#     2.4 Proportion des acteurs/actrices

# In[3]:


actor = tabTitlePrincipal.loc[tabTitlePrincipal['category'] == 'actor'].drop_duplicates(subset = 'nconst')
actor


# In[4]:


actor['nconst'].count()


# In[5]:


actress = tabTitlePrincipal.loc[tabTitlePrincipal['category'] == 'actress'].drop_duplicates(subset = 'nconst')
actress['nconst'].count()


# In[9]:


plt.figure(figsize = (15,10))
data = [1374626,834797]
colors = sns.color_palette('pastel')
plt.pie(data, colors = colors, autopct='%1.2f%%',labels= ['Acteur','Actrice'])
plt.title('Proportion des acteurs/actrices dans la base de données initiale')
plt.savefig('ProportionActeurActrice.png', dpi=300)
plt.show()


#     2.5 Age moyen des acteurs/actrices par décennie

# In[26]:


tabActorActress = tabTitlePrincipal.loc[(tabTitlePrincipal['category'] == 'actor') | (tabTitlePrincipal['category'] == 'actress')]
tabActorActress = pd.merge(tabActorActress, tabNameBasics, how = 'inner', left_on ='nconst', right_on = 'nconst')
tabActorActress = tabActorActress.drop(columns = ['primaryProfession','knownForTitles'])
tabActorActress = tabActorActress.dropna()
tabActorActress                                     


# In[27]:


tabActorActress = pd.merge(tabActorActress, tabTitleBasics, how = 'inner', left_on = 'tconst', right_on = 'tconst')
tabActorActress = tabActorActress.drop(columns = ['titleType','primaryTitle','isAdult','runtimeMinutes','genres'])
tabActorActress = tabActorActress.dropna()
tabActorActress


# In[28]:


tabActorActress['age'] = tabActorActress['startYear'] - tabActorActress['birthYear']
tabActorActress["decade"] = tabActorActress["startYear"]//10*10
tabActorActress


# In[29]:


ageActor = round(tabActorActress.loc[tabActorActress['category'] == 'actor'].groupby('decade')['age'].mean().reset_index())
ageActor = ageActor.drop(index = 0)
ageActor


# In[30]:


ageActress = round(tabActorActress.loc[tabActorActress['category'] == 'actress'].groupby('decade')['age'].mean().reset_index())
ageActress = ageActress.drop(index = 0)
ageActress


# In[22]:


plt.figure(figsize = (15,10))
sns.lineplot(x = ageActor["decade"], y = ageActor["age"], color='lightblue')
sns.lineplot(x = ageActress["decade"], y = ageActress["age"], color='lightpink')
plt.title("Moyenne d'âge des acteurs/actrices par décade")
plt.xlabel("Decade") 
plt.ylabel("Age")
plt.legend(labels = ["Actor","Actress"])
plt.savefig('AgeActorActress.png')
plt.show()


#     2.6 Top 10 acteurs

# In[43]:


top10Actor =pd.DataFrame( tabActorActress.loc[tabActorActress['category'] == 'actor'].groupby('primaryName')['tconst'].count().sort_values(ascending = False).head(10))
top10Actor


#     2.7 Top 10 actrices

# In[44]:


top10Actress =pd.DataFrame( tabActorActress.loc[tabActorActress['category'] == 'actress'].groupby('primaryName')['tconst'].count().sort_values(ascending = False).head(10))
top10Actress


# 3. Export fichier CSV

# In[45]:


tabActorActress.to_csv("tabActorActress.csv", sep = ";")

