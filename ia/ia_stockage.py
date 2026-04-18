import pandas as pd
import joblib
import os

def predire_rupture_stock(nom_produit, stock_actuel, historique_ventes):
    # historique_ventes est une liste des ventes des 30 derniers jours
    df = pd.DataFrame(historique_ventes)
    try:
        if not  historique_ventes or len(historique_ventes) < 2:
            return 0
    except Exception as e:
        print(f"Erreur IA : {e}")
        return 0
    
    # On calcule la moyenne de vente par jour
    consommation_moyenne = df['quantite'].mean()
    
    if consommation_moyenne == 0:
        return "Pas de ventes, stock stable."
    
    # Calcul des jours restants
    jours_restants = stock_actuel / consommation_moyenne
    
    if jours_restants < 3:
        return f"ALERTE : Rupture dans {int(jours_restants)} jours ! Passez commande."
    return f"Stock suffisant pour {int(jours_restants)} jours."


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

