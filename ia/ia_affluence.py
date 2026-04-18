import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

def entrainer_modele_affluence(donnees_historiques):
    
    try:
        if not donnees_historiques or len(donnees_historiques) < 2:
            return 0 
        
    except Exception as e:
        print(f"Erreur IA : {e}")
        return 0
    
    df = pd.DataFrame(donnees_historiques)

    le = LabelEncoder()
    df['saison_n'] = le.fit_transform(df['saison'])

    # 2. CHOIX DES VARIABLES
    
    X = df[['saison_n', 'heure', 'jour_semaine']]
    y = df['niveau_affluence']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    #  RANDOM FOREST CLASSIFIER
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)

    score = model.score(X_test, y_test)
    print(f"Précision de l'IA Affluence : {score * 100:.2f}%")

    return model, le

def predire_foule_actuelle(model, le, saison, heure, jour):
    
    saison_enc = le.transform([saison])[0]
    prediction = model.predict([[saison_enc, heure, jour]])
    
    return prediction[0] # Retourne "Calme", "Moyen" ou "Bondé"

def entrainer_et_sauver_stock(model, nom_fichier="stock_model.pkl"):
    if not os.path.exists('data/modeles_sauvegardes'):
        os.makedirs('data/modeles_sauvegardes')
    
    joblib.dump(model, f'data/modeles_sauvegardes/{nom_fichier}')
    print(f"Modèle sauvegardé dans {nom_fichier}")

def charger_ia_stock(nom_fichier="stock_model.pkl"):
    return joblib.load(f'data/modeles_sauvegardes/{nom_fichier}')
