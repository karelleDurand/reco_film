#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# 1. Import des fichiers

#     1.1 Fichier table title crew

# In[3]:


tabTitleCrew = pd.read_csv("C:/Users/karelle/OneDrive/Documents/Projet 2/Base de données/bds/title.crew.tsv.gz",sep="\t")
tabTitleCrew = tabTitleCrew.drop(columns = "writers")
tabTitleCrew


#     1.2 Fichier table filtrée

# In[6]:


movies_final = pd.read_csv("C:/Users/karelle/OneDrive/Documents/Projet 2/Base de données/fichiers csv/version 2/tabMovieRatingGenreFiltre.csv",
                           sep = ';', index_col = 0)
movies_final.head(5)


#     1.3 Table Name basics

# In[7]:


name_real = pd.read_csv("C:/Users/karelle/OneDrive/Documents/Projet 2/Base de données/bds/name.basics.tsv.gz", sep = '\t')
name_real.head(5)


#    2. Jointure

# In[8]:


tab_director = pd.merge(movies_final,tabTitleCrew, how = "left", left_on = "tconst", right_on = "tconst")


# In[9]:


best_director = tab_director.groupby(["directors"])["tconst"].count().sort_values(ascending = False).head(250).reset_index()
best_director


# In[10]:


tab_best_director = pd.merge(best_director,tabTitleCrew, how = "inner", left_on = "directors", right_on = "directors")
tab_best_director = tab_best_director.drop(columns = ["tconst_x"])
tab_best_director = tab_best_director.rename(columns = {"tconst_y":"tconst"})
tab_best_director


# In[11]:


tab_best_director = pd.merge(tab_best_director,name_real, how = "inner", left_on = "directors", right_on = "nconst")
tab_best_director = tab_best_director.drop(columns = ["nconst","birthYear","deathYear","primaryProfession","knownForTitles"]).drop_duplicates()
tab_best_director


# 3. Export de fichier CSV

# In[12]:


tab_best_director.to_csv("tab_best_director.csv", sep = ";")

