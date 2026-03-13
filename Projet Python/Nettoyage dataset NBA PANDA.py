import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
import seaborn as sns
import os

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

pd.set_option('display.max_columns', 10)  # par exemple, 10 colonnes visibles
pd.set_option('display.width', 100)       # largeur max de l'affichage
pd.set_option('display.max_rows', 20)    # nombre max de lignes visibles
print("Dossier courant :", os.getcwd())

players = pd.read_csv('players.csv')
games_stat = pd.read_csv('games_details.csv')
game_date = pd.read_csv('games.csv')




print("||||||||||||||||||||||||||||||||||||||||||")
print(players.head(),players.columns)
print("#############################")
print(games_stat.head(),games_stat.columns)
print("#############################")
print(game_date.head(),game_date.columns)
print("||||||||||||||||||||||||||||||||||||||||||")


#SELECTION DES 2 DERNIERE SAISON
game_date["GAME_DATE_EST"] = pd.to_datetime(game_date["GAME_DATE_EST"])

game_date = game_date[game_date["GAME_DATE_EST"] >= "2021-12-01"] 
colonnegame = ['GAME_DATE_EST','GAME_ID']
game_date = game_date[colonnegame]
print("#############################")
print("Néttoyage du dataset")



#Nettoyage du dataset game
colonnestat = ['PLAYER_ID','GAME_ID',
       'PLAYER_NAME', 'START_POSITION', 'MIN', 'FGM',
       'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT',
       'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PF', 'PTS',
       'PLUS_MINUS;']
games_stat = games_stat[colonnestat]
#Jointure entre le df game date et le df game stats
#GAME Après 2021 ainsi que les stat des joueurs  sans leurs noms    
games = pd.merge(games_stat,game_date, on='GAME_ID',how = "inner")


#Jointure player name et player id
print(players.columns)
"""
print("------------------------")
print(players[players.duplicated(subset="PLAYER_ID", keep=False)])
print("------------------------")
"""
colonne_players = ['PLAYER_NAME','PLAYER_ID']
players = players[colonne_players]
print("------------------------")
print(players.head())
print("------------------------")

players = players.drop_duplicates(subset="PLAYER_ID")  #note à moi même étape importante pour évité les doublons a la sortit du dataset
player_stats = pd.merge(games,players,on="PLAYER_ID",how = 'inner')
print("#############################")
print("dataset game stats & player id")
######print(player_stats.head(),player_stats.columns)




#Nettoyage des colonnes player id et game id
player_stats = player_stats.drop([ 'GAME_ID','PLAYER_NAME_y'],axis = 1)

print(player_stats.columns)
print(player_stats.shape)
print(player_stats["PLAYER_ID"].nunique())
print(player_stats.head,player_stats.columns)

print(player_stats.dtypes)

players_rolling = (
    player_stats.groupby("PLAYER_NAME_x")[[ 'FGM', 'FGA',
       'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB',
       'DREB', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PF', 'PTS']].rolling(window=3).mean()
       )

print(players_rolling.iloc[2])
print(players_rolling.head)


# Calcul du total de points par joueur
top_scorers = player_stats.groupby("PLAYER_NAME_x")["PTS"].sum().sort_values(ascending=False)

# Affichage des 10 meilleurs scoreurs
print("Top 10 des joueurs qui ont marqué le plus de points depuis décembre 2021 :")
print(top_scorers.head(10))


#Partie ML prediction du nombre de points que l'un joueuer va marquer lors de son prochaine match
# Suppression des lignes avec NaN issues du rolling
players_rolling_clean = players_rolling.dropna().reset_index()# note pour moi pas sur du  .reset_index()

# Features : stats du joueur
X = players_rolling_clean[['FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT',
                           'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB',
                           'AST', 'STL', 'BLK', 'TO', 'PF']]

# Target : points marqués
y = players_rolling_clean['PTS']
player_names = players_rolling_clean['PLAYER_NAME_x']  # noms des joueurs

# Séparer en train/test en conservant le nom
X_train, X_test, y_train, y_test, names_train, names_test = train_test_split(
    X, y, player_names, test_size=0.2, random_state=42
)



# Créer le modèle de régression linéaire
model = LinearRegression()
# Entraînement
model.fit(X_train, y_train)
# Prédictions
y_pred = model.predict(X_test)

# Erreur quadratique moyenne
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse:.2f}")

# Afficher les prédictions avec le nom du joueur et les points réels
pred_df = pd.DataFrame({
    'Player': names_test,
    'Predicted': y_pred,
    'Actual': y_test
})

print("\nTop 10 prédictions :")
print(pred_df.head(10))
