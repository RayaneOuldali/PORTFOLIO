import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns


# Chargement des csv
game = pd.read_csv("game.csv")
game_info = pd.read_csv("game_info.csv")
game_sumary = pd.read_csv("game_summary.csv")


# Afficher les info des csv 
print("===================================")
print(game.columns)
print("-----------------------------------")
print(game_info.columns)
print("-----------------------------------")
print(game_sumary.columns)
print("===================================")


#print(game_info.iloc[-1])
#print(game[ game['game_id'] == game_info.iloc[-1]['game_id']])

#Selectione uniquement les matchs de la saison 2022-2023

game["game_date"] = pd.to_datetime(game["game_date"])
game = game.loc[
(game['game_date']> "2022-10-20") &
(game['game_date']<"2023-04-20")
]

game = game.loc[game["team_abbreviation_home"] =="DEN"] #SELECTION L'equipe de denver ou joue JOKIC AKA Le goat actuelle


#Néttoyage des dataframe

Colonne = ['team_abbreviation_home','game_id','wl_home','fg_pct_home','fg3_pct_home','ft_pct_home', 'oreb_home', 'dreb_home',
       'reb_home', 'ast_home', 'stl_home', 'blk_home','pts_home', 'plus_minus_home','game_id','wl_away','fg_pct_away', 'fg3_pct_away','ft_pct_away','oreb_away',
       'dreb_away', 'reb_away', 'ast_away', 'stl_away', 'blk_away','pts_away', 'plus_minus_away']




col_existante = [i for i in Colonne if i in game.columns]#columns
game = game.loc[:,col_existante]


"""
#game = gameHome.join(gameAway, how = 'inner')
print(type(gameHome['pts_home']))
print("==================================================")
#Trouver les équipes qui score le plus et celles qui score le moins 
gameHome['RowPts'] = gameHome.groupby("team_abbreviation_home")
gameHome['RowPts'] = gameHome['pts_home'].rolling(window= 20).mean()
print(gameHome['RowPts'])
"""
#Affichage des stats de la saison des denver nuggets 
print("=========Affichage des stats de la saison des denver nuggets=========")
print("=========dataset.head()=========")
print(game.head())
print("=========dataset.describe()=========")
print(game.describe())
sns.scatterplot(game["pts_home","pts_away"])














