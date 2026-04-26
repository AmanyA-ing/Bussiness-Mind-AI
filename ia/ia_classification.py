import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from database import SessionLocal
import models
import joblib
import os

def classer_importance_stock(donnees_historiques):
    # ... ton code de calcul ...
    db = SessionLocal()
    ventes = db.query(models.Vente).all()
    
    df = pd.DataFrame([
        {"produit": v.produit_nom, "quantite": v.quantite, "benefice": v.benefice_total} 
        for v in ventes
    ])
    
    seuil_benefice = df['benefice'].median()
    df['top_produit'] = ((df['benefice'] > seuil_benefice)).astype(int)
    
    le = LabelEncoder()
    df['produit_n'] = le.fit_transform(df['produit'])
    
    X = df[['produit_n', 'quantite']]
    y = df['top_produit']
    
    clf = RandomForestClassifier()
    clf.fit(X, y)
    
    return clf, le # Retourne le modèle et l'encodeur

def sauver_modele_vip(model, nom_fichier="vip_stock_model.pkl"):
    if not os.path.exists('data/modeles_sauvegardes'):
        os.makedirs('data/modeles_sauvegardes')
    joblib.dump(model, f'data/modeles_sauvegardes/{nom_fichier}')
    print(f"Modèle VIP sauvegardé : {nom_fichier}")