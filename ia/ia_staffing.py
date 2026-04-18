import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from database import SessionLocal
import models
import joblib
import os
def calculer_besoin_caissiers(heure_test):
    try:
        if not heure_test or len(heure_test) < 2:
            return 0 # Retourne 0 au lieu de faire planter l'app
            
    except Exception as e:
        print(f"Erreur IA : {e}")
        return 0
    
    db = SessionLocal()
    ventes = db.query(models.Vente).all()
    
    # On crée un historique : Heure -> Nombre de clients (tickets uniques)
    data = [{"heure": v.date_heure.hour, "ticket": v.ticket_numero} for v in ventes]
    df = pd.DataFrame(data)
    
    # On compte combien de tickets par heure dans l'histoire
    stats = df.groupby('heure')['ticket'].nunique().reset_index()
    
    X = stats[['heure']]
    y = stats['ticket']
    
    # IA Forest pour prédire l'affluence
    model = RandomForestRegressor(n_estimators=100)
    model.fit(X, y)
    
    prediction_clients = model.predict([[heure_test]])[0]
    
    # LOGIQUE MÉTIER 
    if prediction_clients < 10:
        nb_caissiers = 1
    elif prediction_clients < 30:
        nb_caissiers = 2
    else:
        nb_caissiers = 4
        
    return int(nb_caissiers)


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
