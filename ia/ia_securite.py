from sklearn.ensemble import IsolationForest
import numpy as np
import joblib
import os

def detecter_fraude(transactions_du_jour,donnees):
    try:
        if not transactions_du_jour or len(transactions_du_jour) < 2:
            return 0 # Retourne 0 au lieu de faire planter l'app
            
    except Exception as e:
        print(f"Erreur IA : {e}")
        return 0
    
    # On analyse : [Heure, Montant, Quantité]
    data = np.array(transactions_du_jour)
    
    # Le modèle apprend ce qui est "normal"
    model = IsolationForest(contamination=0.05) # On estime 5% d'anomalies max
    model.fit(data)
    
    # -1 signifie que c'est une anomalie (fraude potentielle)
    predictions = model.predict(data)
    
    anomalies = [i for i, x in enumerate(predictions) if x == -1]
    return anomalies # Liste des indices des ventes suspectes

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

