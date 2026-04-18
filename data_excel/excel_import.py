import pandas as pd
from sqlalchemy.orm import Session
from database import SessionLocal
import models
from datetime import datetime

def import_historique_excel(chemin_fichier):
    db = SessionLocal()

    df = pd.read_excel(chemin_fichier)

    # 2. Le Mapping (On traduit l'utilisateur vers ton code)
    # A gauche : ce que l'utilisateur a écrit dans Excel
    # A droite : le nom officiel dans ton models.py
    mapping_colonnes = {
        "Article": "produit_nom",
        "Produit": "produit_nom",
        "Type": "categorie",
        "Rayon": "categorie",
        "Prix_Vnt": "prix_vente",
        "Qte": "quantite",
        "Vendeur": "caissier_nom"
    }
    df = df.rename(columns=mapping_colonnes)

    # 3. Boucle d'enregistrement
    for index, row in df.iterrows():
        # On vérifie si on a le prix d'achat dans le catalogue
        # Sinon on met une valeur par défaut pour ne pas bloquer
        nom_p = str(row['produit_nom']).lower().strip()
        
        # On déduit la saison automatiquement à partir de la date du Excel
        date_vente = pd.to_datetime(row['Date'])
        mois = date_vente.month
        saison_auto = "Saison des pluies" if (4 <= mois <= 7 or 10 <= mois <= 11) else "Saison sèche"

        nouvelle_vente = models.Vente(
            ticket_numero=f"HISTO-{index}",
            produit_nom=nom_p,
            categorie=row.get('categorie', 'Divers'),
            quantite=row['quantite'],
            prix_vente=row['prix_vente'],

            prix_total=row['prix_vente'] * row['quantite'],
            caissier_nom=row.get('caissier_nom', 'Ancien Système'),
            date_heure=date_vente,
            saison=saison_auto
        )
        db.add(nouvelle_vente)

    db.commit()
    db.close()
    print("✅ Historique importé avec succès !")

if __name__ == "__main__":

    pass