#!/usr/bin/env python
# coding: utf-8

# In[2]:


import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import datetime as dt


# 1. Import des tables

#     1.1 Table Akas

# In[3]:


#Import de la table title.akas
#Remplacement des \N par Nan
#Filtrer sur les régions = 'FR' avec le chunk
iter_csv=pd.read_csv("C:/Users/karelle/OneDrive/Documents/Projet 2/Base de données/bds/title.akas.tsv.gz",sep="\t",
                     index_col="titleId",
                     na_values="\\N", 
                     keep_default_na=True,
                     usecols=['titleId','title','region'],
                     chunksize=1000)
tabTitleAka = pd.concat([chunk[chunk['region'] == 'FR'] for chunk in iter_csv])
#Suppression de la colonne 'region'
tabTitleAka=tabTitleAka.drop(columns=['region']).reset_index()
tabTitleAka


#     1.2 Table TitleBasics

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


#     1.3 Table Rating

# In[5]:


#Import de la table title.ratings
#Remplace les \N par des NaN
tabTitleRating=pd.read_csv("C:/Users/karelle/OneDrive/Documents/Projet 2/Base de données/bds/title.ratings.tsv.gz",sep="\t",
                           na_values="\\N",
                           engine='c',
                           index_col="tconst",
                           low_memory=True)
tabTitleRating


# In[6]:


tabTitleRating = tabTitleRating.reset_index()
tabTitleRating


# 2. Jointure des tables Akas et TitleBasics

# In[7]:


#jointure pour avoir tous les films 'FR' et 'movie'
table_movie = pd.merge(tabTitleAka,tabTitleBasics, how = 'inner', left_on = 'titleId', right_on = 'tconst')
table_movie = table_movie.drop_duplicates(keep = 'last').drop(columns = 'titleId')
tab1 = table_movie.loc[(table_movie['title'].str.contains('Épisode #'))]
table_movie = table_movie.drop(index=tab1.index)
tab2 = table_movie.loc[(table_movie['title'].str.contains('Épisode datant'))]
table_movie = table_movie.drop(index=tab2.index)
table_movie


# In[210]:


table_movie.info()


# 3. Jointure entre table_movie et tableRating

# In[8]:


table_movieRating = pd.merge(table_movie,tabTitleRating, how = 'inner', left_on = 'tconst', right_on = 'tconst')
table_movieRating = table_movieRating.drop_duplicates(keep = 'last')
table_movieRating


# In[9]:


table_movieRating.fillna(0, inplace = True)
table_movieRating


# 4. Split des genres

# In[10]:


table_movieRating[['one','two','three']] = table_movieRating.genres.str.split(',',expand=True)
table_movieRating


# In[11]:


genre_one = pd.DataFrame(pd.get_dummies(table_movieRating['one'])).astype(int)
genre_one.sum()


# In[12]:


genre_two = pd.DataFrame(pd.get_dummies(table_movieRating['two'])).astype(int)
genre_two.insert(0, "Action", 0, allow_duplicates=False)
genre_two.sum()


# In[13]:


genre_three = pd.DataFrame(pd.get_dummies(table_movieRating['three'])).astype(int)
genre_three.insert(0, "Action", 0, allow_duplicates=False)
genre_three.insert(1, "Adult", 0, allow_duplicates=False)
genre_three.insert(2, "Adventure", 0, allow_duplicates=False)
genre_three.sum()


# In[14]:


genre = genre_one | genre_two | genre_three
genre = genre.fillna(0).astype(int).drop(columns = 'Autres')
genre.sum()


# In[15]:


table_movieRating = pd.merge(table_movieRating, genre, left_index = True, right_index = True)
table_movieRating


# In[16]:


table_movieRating.drop(columns = ['one','two','three'], inplace = True)
table_movieRating.info()


# 5. export en fichier CSV

# In[220]:


table_movieRating.to_csv("table_movieRatingGenre.csv", sep = ";")


# 6. Graphique

#     6.1 Nombre de votes en fonction de la durée des films

# In[221]:


plt.figure(figsize = (15,10))
sns.scatterplot(data = table_movieRating, x = 'runtimeMinutes', y = 'numVotes', color = 'lightblue')
plt.title('Nombre de votes en fonction de la durée des films')
plt.xlabel('Durée des films')
plt.ylabel('Nombre de votes')
plt.xlim([0, 400])
plt.xticks(np.arange(0,400,15))
plt.savefig('NombreVoteDurée.png', dpi=300)
plt.show()


#     6.2 Nombre de votes en fonction du genre

# In[222]:


colonne = table_movieRating.columns
colonne = colonne[8:]
dico ={}
vote = 0
for i in colonne :
    vote = table_movieRating.loc[table_movieRating[i] == 1, 'numVotes'].sum()
    dico.update({i : vote})
nombreVote = pd.DataFrame(list(dico.items()), columns=['genres', 'count'])
nombreVote


# In[223]:


plt.figure(figsize = (15,10))
sns.barplot(data = nombreVote, x = 'genres', y = 'count', color = 'lightblue')
plt.title('Nombre de votes en fonction des genres de films')
plt.xlabel('Genre')
plt.ylabel('Count')
plt.xticks(rotation = 90)
plt.savefig('NombreVoteParGenre.png', dpi=300)
plt.show()


#     6.3 Note moyenne en fonction des genres

# In[224]:


colonne = table_movieRating.columns
colonne = colonne[8:]
dico ={}
note = 0
for i in colonne :
    note = table_movieRating.loc[table_movieRating[i] == 1, 'averageRating'].mean()
    dico.update({i : note})
noteMoyenne = round(pd.DataFrame(list(dico.items()), columns=['genres', 'count']),1)
noteMoyenne


# In[225]:


plt.figure(figsize = (15,10))
sns.barplot(data = noteMoyenne, x = 'genres', y = 'count', color = 'lightblue')
plt.title('Note moyenne en fonction des genres de films')
plt.xlabel('Genre')
plt.ylabel('Count')
plt.xticks(rotation = 90)
plt.savefig('NoteParGenre.png', dpi=300)
plt.show()


#     6.4 Répartition des genres dans movie

# In[226]:


colonne = table_movieRating.columns
colonne = colonne[8:]
dico ={}
count = 0
for i in colonne :
    count = table_movieRating.loc[table_movieRating[i] == 1, i].sum()
    dico.update({i : count})
countGenre = pd.DataFrame(list(dico.items()), columns=['genres', 'count']).sort_values(by = 'count', ascending = False)
countGenre


# In[227]:


plt.figure(figsize = (15,10))
sns.barplot(data = countGenre, x = 'genres', y = 'count', color = 'lightblue')
plt.title('Répartition des genres de films')
plt.xlabel('Genre')
plt.ylabel('Count')
plt.xticks(rotation = 90)
plt.savefig('RépartitionGenre.png', dpi=300)
plt.show()


#     6.5 Top 10 des films selon le nombre de vote

# In[228]:


top10Vote = table_movieRating.sort_values(by = 'numVotes', ascending = False).head(10)[['title','numVotes']]
top10Vote


#     6.6 Top 10 des films selon la note moyenne

# In[229]:


top10Note = table_movieRating.sort_values(by = 'averageRating', ascending = False).head(10)[['title','averageRating']]
top10Note


#     6.7 Nombre de films par décade

# In[17]:


nbr_sortie_film=pd.DataFrame(table_movieRating["startYear"]//10*10).value_counts().sort_index().reset_index().rename({0:'count'},axis=1)
nbr_sortie_film=nbr_sortie_film.drop(index=0)
nbr_sortie_film


# In[18]:


plt.figure(1, figsize=(15,10))
sns.barplot(nbr_sortie_film['startYear'],nbr_sortie_film['count'], color='lightblue')
plt.title("Nombre de sortie de films par décennie")
plt.ylabel('Fréquence')
plt.xlabel('Décennie')
plt.savefig('NombreSortieBydecenie.png', dpi=300)
plt.show()


#     6.8 Durée moyenne des films par décennie

# In[19]:


table_movieRating['runtimeMinutes'] = table_movieRating['runtimeMinutes'].astype(int)
tab1 = table_movieRating.loc[table_movieRating['runtimeMinutes'] == 0]
tab2 = table_movieRating.drop(index = tab1.index)
duree_film=pd.DataFrame(tab2.groupby(tab2['startYear']//10*10)['runtimeMinutes'].mean()).reset_index()
duree_film=duree_film.drop(index=0)
duree_film


# In[20]:


plt.figure(1, figsize=(15,10))
sns.barplot(duree_film['startYear'],duree_film['runtimeMinutes'], color='lightblue')
plt.title("Durée moyenne des films par décennie")
plt.ylabel('Durée moyenne')
plt.xlabel('Décennie')
plt.savefig('DuréeByDecennie.png', dpi=300)
plt.show()

