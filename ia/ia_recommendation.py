import pandas as pd
from database import SessionLocal
import models
import datetime
def suggerer_produit(nom_produit_actuel,donnees):
    try:
        if not donnees or len(donnees) < 2:
            return 0 # Retourne 0 au lieu de faire planter l'app
            
    except Exception as e:
        print(f"Erreur IA : {e}")
        return 0
    
    db = SessionLocal()
    # On récupère toutes les lignes de ventes pour analyser les paniers
    ventes = db.query(models.Vente).all()
    df = pd.DataFrame([{"ticket": v.ticket_numero, "produit": v.produit_nom} for v in ventes])
    
    # 1. Trouver tous les tickets qui contiennent le produit actuel
    tickets_contenant_produit = df[df['produit'] == nom_produit_actuel.lower()]['ticket'].unique()
    
    # 2. Trouver les autres produits dans ces mêmes tickets
    autres_achats = df[df['ticket'].isin(tickets_contenant_produit) & (df['produit'] != nom_produit_actuel.lower())]
    
    if not autres_achats.empty:
        # On prend le produit le plus fréquent
        recommandation = autres_achats['produit'].value_counts().idxmax()
        return f"Conseil : Proposez '{recommandation.upper()}' au client !"
    
    return "Pas encore de recommandation pour ce produit."

def obtenir_suggestion_complete(nom_produit):
    db = SessionLocal()
    maintenant = datetime.now()
    nom_clean = nom_produit.lower().strip()
    
    # --- ÉTAPE A : LA PROMO (Est-ce qu'il y a une réduction ?) ---
    promo = db.query(models.Promotion).filter(
        models.Promotion.produit_nom == nom_clean,
        models.Promotion.date_debut <= maintenant,
        models.Promotion.date_fin >= maintenant
    ).first()
    
    msg_promo = ""
    if promo:
        msg_promo = f"🔥 ALERTE PROMO : Ce produit est à -{promo.reduction_pourcent}% !"

    # --- ÉTAPE B : LE COMPLÉMENT (Quoi vendre avec ?) ---
    # On regarde ce que les autres ont acheté avec ce produit
    ventes_historiques = db.query(models.Vente).all()
    df = pd.DataFrame([{"ticket": v.ticket_numero, "p": v.produit_nom} for v in ventes_historiques])
    
    tickets_clients = df[df['p'] == nom_clean]['ticket'].unique()
    suggestions = df[df['ticket'].isin(tickets_clients) & (df['p'] != nom_clean)]
    
    msg_suggest = ""
    if not suggestions.empty:
        meilleur_choix = suggestions['p'].value_counts().idxmax()
        msg_suggest = f"💡 IA : Les clients prennent souvent '{meilleur_choix}' avec ça."

    return {
        "promo": msg_promo,
        "suggestion": msg_suggest,
        "phrase_caissier": f"{msg_promo} {msg_suggest}"
    }