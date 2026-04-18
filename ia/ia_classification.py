import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from database import SessionLocal
import models
import joblib
import os
def classer_importance_stock(donnees_historiques):
    try:
        if not donnees_historiques or len(donnees_historiques) < 2:
            return 0 
        
    except Exception as e:
        print(f"Erreur IA : {e}")
        return 0
    
    db = SessionLocal()
    ventes = db.query(models.Vente).all()
    
    df = pd.DataFrame([
        {"produit": v.produit_nom, "quantite": v.quantite, "benefice": v.benefice_total} 
        for v in ventes
    ])
    
    # 1 si le produit rapporte beaucoup ET se vend vite, sinon 0
    seuil_benefice = df['benefice'].median()
    df['top_produit'] = ((df['benefice'] > seuil_benefice)).astype(int)
    
    le = LabelEncoder()
    df['produit_n'] = le.fit_transform(df['produit'])
    
    X = df[['produit_n', 'quantite']]
    y = df['top_produit']
    
    clf = RandomForestClassifier()
    clf.fit(X, y)
    
    return "Modèle de classification prêt : Identification des produits VIP terminée."
    

def entrainer_et_sauver_stock(model, nom_fichier="stock_model.pkl"):
    # On crée le dossier s'il n'existe pas
    if not os.path.exists('data/modeles_sauvegardes'):
        os.makedirs('data/modeles_sauvegardes')
    
    # On sauvegarde le "cerveau" de l'IA dans un fichier
    joblib.dump(model, f'data/modeles_sauvegardes/{nom_fichier}')
    print(f"Modèle sauvegardé dans {nom_fichier}")

def charger_ia_stock(nom_fichier="stock_model.pkl"):
    # On recharge le cerveau instantanément sans recalculer
    return joblib.load(f'data/modeles_sauvegardes/{nom_fichier}')
