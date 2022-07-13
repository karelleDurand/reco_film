#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np


# 1. Import des fchiers CSV

#     1.1 Table filtrée

# In[3]:


movies_final = pd.read_csv("C:/Users/karelle/OneDrive/Documents/Projet 2/Base de données/fichiers csv/version 2/tabMovieRatingGenreFiltre.csv", sep = ';', index_col = 0)
movies_final


#     1.2 Table réalisateurs

# In[4]:


best_director = pd.read_csv("C:/Users/karelle/OneDrive/Documents/Projet 2/Base de données/fichiers csv/version 2/tab_best_director.csv", sep = ';', index_col = 0)
best_director


#     1.3 Table du pays d'origine des films

# In[10]:


language = pd.read_csv("C:/Users/karelle/OneDrive/Documents/Projet 2/Base de données/fichiers csv/version 2/movies_metadata.csv", sep =',', usecols= ['imdb_id','original_language'])
language = language.dropna()
language.head(5)


# 2. Jointure

# In[7]:


tab_movies_director = pd.merge(movies_final,best_director, how = "left", left_on = "tconst", right_on = "tconst")
tab_movies_director = tab_movies_director.fillna(0)
tab_movies_director


# In[14]:


tab_movies_director= pd.get_dummies(data = tab_movies_director,columns = ['primaryName'], prefix = "", sparse = True)
tab_movies_director


# In[16]:


tab_genre_dir_lang = pd.merge(tab_movies_director,language, how = "left", left_on = "tconst", right_on = "imdb_id").drop(columns = "imdb_id")
tab_genre_dir_lang = tab_genre_dir_lang.fillna(0)
tab_genre_dir_lang.head(5)


# In[17]:


tab_genre_dir_lang= pd.get_dummies(data = tab_genre_dir_lang,columns = ['original_language'], prefix = "", sparse = True)
tab_genre_dir_lang.head(5)


# In[18]:


table_KNN = tab_genre_dir_lang.drop(columns = "_0")
table_KNN.drop_duplicates()
table_KNN


# 3. Export fichier CSV

# In[19]:


table_KNN.to_csv("table_KNN.csv",sep = ";")

