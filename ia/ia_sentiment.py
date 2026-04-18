from textblob import TextBlob
import joblib
import os

def score_sentiment(texte):
    
    if not texte or texte.strip() == "":
        return 0.0 # Neutre si pas de commentaire
    
    # TextBlob analyse la polarité (positif/négatif)
    blob = TextBlob(texte)
    return blob.sentiment.polarity

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