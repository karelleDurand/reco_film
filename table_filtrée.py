#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import datetime as dt


# 1. Import des fichiers CSV

#     1.2 Fichier table_movieRatingGenre

# In[2]:


table_movieRatingGenre = pd.read_csv("C:/Users/karelle/OneDrive/Documents/Projet 2/Base de données/fichiers csv/version 2/table_movieRatingGenre.csv",sep=';')
table_movieRatingGenre = table_movieRatingGenre.drop(columns = 'Unnamed: 0')
table_movieRatingGenre


#     1.2 Fichier tabActorActress

# In[3]:


tabActorActress = pd.read_csv("C:/Users/karelle/OneDrive/Documents/Projet 2/Base de données/fichiers csv/version 2/tabActorActress.csv",sep=';')
tabActorActress = tabActorActress.drop(columns = 'Unnamed: 0')
tabActorActress


# 2. Application des filtres

#     2.1 Par la durée des films

# In[4]:


duréeNulle = table_movieRatingGenre.loc[table_movieRatingGenre['runtimeMinutes'] == 0]
table_movieRatingGenre = table_movieRatingGenre.drop(index = duréeNulle.index)
table_movieRatingGenre


# In[5]:


table_movieRatingGenre['runtimeMinutes'].describe(percentiles = np.arange(0,1,0.1))


# In[6]:


table_movieRatingGenre['runtimeMinutes'] = table_movieRatingGenre['runtimeMinutes'].astype(int)
table_movieRatingGenre.info()


# In[7]:


table_movieRatingGenre = table_movieRatingGenre.loc[(table_movieRatingGenre['runtimeMinutes'] >= 85)]
table_movieRatingGenre = table_movieRatingGenre.loc[(table_movieRatingGenre['runtimeMinutes'] <= 245)]
table_movieRatingGenre


#     2.2 Par la note moyenne

# In[8]:


table_movieRatingGenre['averageRating'].describe(percentiles = np.arange(0,1,0.1))


# In[9]:


noteMoyenne = table_movieRatingGenre.loc[table_movieRatingGenre['averageRating'] < 4]
table_movieRatingGenre = table_movieRatingGenre.drop(index = noteMoyenne.index)
table_movieRatingGenre


#     2.3 Par le nombre de votes

# In[10]:


table_movieRatingGenre['numVotes'].describe(percentiles = np.arange(0,1,0.1))


# In[11]:


nombreVote = table_movieRatingGenre.loc[table_movieRatingGenre['numVotes'] < 589]
table_movieRatingGenre = table_movieRatingGenre.drop(index = nombreVote.index)
table_movieRatingGenre


#     2.4 Par la décade

# In[12]:


table_movieRatingGenre["decade"] = table_movieRatingGenre["startYear"]//10*10
table_movieRatingGenre


# In[13]:


table_movieRatingGenre["decade"].describe(percentiles = np.arange(0,1,0.1))


# In[14]:


decade = table_movieRatingGenre.loc[table_movieRatingGenre["decade"] < 1970]
table_movieRatingGenre = table_movieRatingGenre.drop(index = decade.index)
table_movieRatingGenre


# 3. Export de la table filtrée

# In[41]:


table_movieRatingGenre.to_csv("tabMovieRatingGenreFiltre.csv", sep = ";")


# 4.Graphique

#     4.1 Nombre de fimls par décade

# In[58]:


nbr_sortie_film=pd.DataFrame(table_movieRatingGenre.groupby('decade')['tconst'].count().sort_index().reset_index())
nbr_sortie_film


# In[59]:


plt.figure(1, figsize=(15,10))
sns.barplot(nbr_sortie_film['decade'],nbr_sortie_film['tconst'], color='lightblue')
plt.title("Nombre de sortie de films par décennie")
plt.ylabel('Fréquence')
plt.xlabel('Décennie')
plt.savefig('NombreSortieBydecenieFiltre.png', dpi=300)
plt.show()


#     4.2 Prédiction pourla décennie 2020

# In[60]:


nbr_sortie_film = nbr_sortie_film.drop(index = 5)
sns.regplot(data=nbr_sortie_film,x='decade',y='tconst')
plt.show()


# In[61]:


from sklearn.linear_model import LinearRegression
X = nbr_sortie_film[['decade']] 
y = nbr_sortie_film['tconst'] 
modelLR = LinearRegression().fit(X, y)
print("Scikit-Learn :  ", modelLR.predict([[2020]])  )


# In[62]:


nbr_sortie_film.loc[5] = [2020,9640]
nbr_sortie_film


# In[63]:


plt.figure(1, figsize=(15,10))
sns.barplot(nbr_sortie_film['decade'],nbr_sortie_film['tconst'], color='lightblue')
plt.title("Prévision sur la décennie 2020")
plt.ylabel('Fréquence')
plt.xlabel('Décennie')
plt.savefig('Prévision2020.png', dpi=300)
plt.show()


#     4.3 Top 10 acteurs

# In[34]:


tableMovieActorActress = pd.merge(table_movieRatingGenre, tabActorActress, how = 'left', left_on = 'tconst', right_on = 'tconst').drop_duplicates().reset_index()
tableMovieActorActress = tableMovieActorActress.drop(columns = 'index')
tableMovieActorActress


# In[40]:


tableMovieActor = pd.DataFrame(tableMovieActorActress.loc[tableMovieActorActress['category'] == 'actor'].groupby('primaryName')['tconst'].count().sort_values(ascending = False).head(10)).reset_index()
tableMovieActor


# In[53]:


plt.figure(1, figsize=(15,10))
sns.barplot(tableMovieActor['primaryName'],tableMovieActor['tconst'], color='lightblue')
plt.title("Top 10 des acteurs")
plt.ylabel('Nombre de films')
plt.xlabel('Acteurs')
plt.xlim([-1, 10])
plt.xticks(rotation = 90)
plt.savefig('Top10ActorFiltre.png', dpi=300)
plt.show()


#     4.4 Top 10 actrices

# In[55]:


tableMovieActress = pd.DataFrame(tableMovieActorActress.loc[tableMovieActorActress['category'] == 'actress'].groupby('primaryName')['tconst'].count().sort_values(ascending = False).head(10)).reset_index()
tableMovieActress


# In[57]:


plt.figure(1, figsize=(15,10))
sns.barplot(tableMovieActress['primaryName'],tableMovieActor['tconst'], color='lightblue')
plt.title("Top 10 des actrices")
plt.ylabel('Nombre de films')
plt.xlabel('Actrices')
plt.xlim([-1, 10])
plt.xticks(rotation = 90)
plt.savefig('Top10ActressFiltre.png', dpi=300)
plt.show()

