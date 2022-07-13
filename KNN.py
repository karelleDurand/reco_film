#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors


# In[26]:


table_KNN = pd.read_csv("C:/Users/karelle/OneDrive/Documents/Projet 2/Base de données/fichiers csv/version 2/table_KNN.csv", sep = ';', index_col = 0)
table_KNN = table_KNN.drop(columns = ['genres','decade','directors'])
table_KNN


# In[33]:


# définition des X et y
X = table_KNN.drop(columns=['title','tconst','primaryTitle'])

# standardisation
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled = pd.DataFrame(X_scaled, columns = X.columns)

X_scaled_poids = pd.DataFrame(X_scaled)

#attribution des poids
X_scaled_poids["numVotes"] = X_scaled_poids["numVotes"]*0.9
X_scaled_poids["averageRating"] = X_scaled_poids["averageRating"]*0.9
X_scaled_poids["runtimeminutes"] = X_scaled_poids["runtimeMinutes"]*0.9
X_scaled_poids["startyear"] = X_scaled_poids["startYear"]*0.9
X_scaled_poids.iloc[:,7:8] = X_scaled_poids.iloc[:,7:8]*0.7             #action
X_scaled_poids.iloc[:,9:10] = X_scaled_poids.iloc[:,9:10]*0.3           #aventure
X_scaled_poids.iloc[:,10:11] = X_scaled_poids.iloc[:,10:11]*0.5         #animation
X_scaled_poids.iloc[:,12:13] = X_scaled_poids.iloc[:,12:13]*0.1         #comedie
X_scaled_poids.iloc[:,13:14] = X_scaled_poids.iloc[:,13:14]*0.5         #crime
X_scaled_poids.iloc[:,14:15] = X_scaled_poids.iloc[:,14:15]*0.5         #documentaire
X_scaled_poids.iloc[:,15:16] = X_scaled_poids.iloc[:,15:16]*0.1         #drame
X_scaled_poids.iloc[:,16:17] = X_scaled_poids.iloc[:,16:17]*0.4         #family
X_scaled_poids.iloc[:,24:25] = X_scaled_poids.iloc[:,24:25]*0.3         #mistère
X_scaled_poids.iloc[:,28:29] = X_scaled_poids.iloc[:,28:29]*0.3         #sci_fi
X_scaled_poids.iloc[:,35:285] = X_scaled_poids.iloc[:,35:285]*0.4       #réalisateurs
X_scaled_poids.iloc[:,285:] = X_scaled_poids.iloc[:,285:]*0.4           #pays d'origine


#KNN
end_of_game=False
while not end_of_game:
    film = str(input("Entrez un titre de film : "))
    if pd.DataFrame(table_KNN["title"].str.contains(film, case=False)).any()[0]!=True:
        end_of_game=False
    else:
        indice = table_KNN.loc[table_KNN["title"].str.contains(film, case=False)].index[0]
        distanceKNN = NearestNeighbors(n_neighbors=9, metric='minkowski', p=2).fit(X_scaled_poids)
        dist = distanceKNN.kneighbors(X_scaled_poids.loc[[indice]])
        proposition = table_KNN.loc[list(dist[1][0])].drop(index=indice).head(5)
        print(indice)
        break
print(table_KNN.loc[table_KNN.index[indice]])
proposition[["title","startYear","runtimeMinutes","averageRating","numVotes"]]


# In[ ]:


#détermination du poids des colonnes
poids_vote = 0.1
dist_min_vote = {}
for poids_vote in np.arange(0.1,1.1,0.1) :
    X_scaled_poids.iloc[:,285:] = X_scaled_poids.iloc[:,285:]*poids_vote
    #print(X_scaled_poids)
    indice = table_KNN.loc[table_KNN["title"].str.contains('iron man', case=False)].index[0]
    distanceKNN = NearestNeighbors(n_neighbors=6).fit(X_scaled_poids)
    dist = distanceKNN.kneighbors(X_scaled_poids.loc[[indice]])
    dist_dist = list(np.delete(dist[0][0],[0]))
    dist_indice = np.delete(dist[1][0],[0])
    #dist_min_vote.append(dist_dist)
    dist_min_vote.update( {poids_vote : dist_dist} )
from heapq import nsmallest
from operator import itemgetter

#get the N smallest members
smallestN = nsmallest(1, dist_min_vote.items(), itemgetter(1))
print(smallestN)

