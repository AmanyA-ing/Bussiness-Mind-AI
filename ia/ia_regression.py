import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib
import os

def predire_prix_total(donnees_ventes):
    try:
        if not donnees_ventes or len(donnees_ventes) < 2:
            return 0 
    except Exception as e:
        print(f"Erreur IA : {e}")
        return 0
    
    df = pd.DataFrame(donnees_ventes)

    le = LabelEncoder()
    df['saison_n'] = le.fit_transform(df['saison'])

    # 2. CHOIX DES VARIABLES (Ce que tu m'as listé)
    # X = les caractéristiques, y = ce qu'on veut deviner (Prix Total)
    X = df[['saison_n', 'quantite', 'heure', 'prix_unitaire']]
    y = df['prix_total']

    # TRAIN-TEST SPLIT 
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # RANDOM FOREST 
    model = RandomForestRegressor(n_estimators=100)
    model.fit(X_train, y_train)

    score = model.score(X_test, y_test)
    print(f"Précision du modèle : {score * 100:.2f}%")

    return model

def entrainer_et_sauver_stock(model, nom_fichier="stock_model.pkl"):
    if not os.path.exists('data/modeles_sauvegardes'):
        os.makedirs('data/modeles_sauvegardes')
    
    # On sauvegarde le "cerveau" de l'IA dans un fichier
    joblib.dump(model, f'data/modeles_sauvegardes/{nom_fichier}')
    print(f"Modèle sauvegardé dans {nom_fichier}")

def charger_ia_stock(nom_fichier="stock_model.pkl"):
    # On recharge le cerveau instantanément sans recalculer
    return joblib.load(f'data/modeles_sauvegardes/{nom_fichier}')
