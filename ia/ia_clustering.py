import pandas as pd
from sklearn.cluster import KMeans
from database import SessionLocal
import models
import joblib
import os

def grouper_produits_similaires(donnees_historiques):
    try:
        if not donnees_historiques or len(donnees_historiques) < 2:
            return 0 # Retourne 0 au lieu de faire planter l'app
            
    except Exception as e:
        print(f"Erreur IA : {e}")
        return 0
    db = SessionLocal()
    # On regarde le prix de vente moyen et la quantité totale vendue par produit
    query = "SELECT produit_nom, AVG(prix_vente) as prix, SUM(quantite) as qte_totale FROM ventes GROUP BY produit_nom"
    df = pd.read_sql(query, db.bind)
    
    X = df[['prix', 'qte_totale']]
    
    kmeans = KMeans(n_clusters=3) # 3 groupes : Petits prix/Gros volume, Luxe, Moyen
    df['cluster'] = kmeans.fit_predict(X)
    
    return df[['produit_nom', 'cluster']]

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
