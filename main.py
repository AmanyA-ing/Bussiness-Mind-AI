from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import models
from database import SessionLocal, engine
from passlib.context import CryptContext

app = FastAPI(title="Smart Retail System - Abidjan")

# Connexion à la base
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#  FONCTIONS AUTOMATIQUES 

def obtenir_saison():
    mois = datetime.now().month
    # Saison des pluies en Côte d'Ivoire (Avr-Juil, Oct-Nov)
    if (4 <= mois <= 7) or (10 <= mois <= 11):
        return "Saison des pluies"
    return "Saison sèche"

def obtenir_moment():
    heure = datetime.now().hour
    if 6 <= heure < 12: return "Matin"
    if 12 <= heure < 18: return "Après-midi"
    return "Soir"

def calculer_prix_automatique(nom_produit, db: Session):
    # 1. On cherche le prix de base dans le catalogue
    produit = db.query(models.ProduitCatalogue).filter(
        models.ProduitCatalogue.produit_nom == nom_produit.lower()
    ).first()
    
    if not produit:
        return None # Produit inconnu

    prix_final = produit.prix_vente_base

    # 2. On vérifie s'il y a une promo active pour ce produit AUJOURD'HUI
    maintenant = datetime.now()
    promo = db.query(models.Promotion).filter(
        models.Promotion.produit_nom == nom_produit.lower(),
        models.Promotion.date_debut <= maintenant,
        models.Promotion.date_fin >= maintenant,
        models.Promotion.active == True
    ).first()

    # 3. On applique la réduction si elle existe
    if promo:
        reduction = (prix_final * promo.reduction_pourcent) / 100
        prix_final = prix_final - reduction
        print(f"Promo appliquée : -{promo.reduction_pourcent}%")

    return prix_final

# --- ROUTES DE VENTE (Pour le Caissier) ---
@app.post("/caissier/vendre")
def enregistrer_vente(nom_produit: str, quantite: int, db: Session = Depends(get_db)):
    # 1. On cherche le produit dans le catalogue (Le prix de référence)
    produit_info = db.query(models.ProduitCatalogue).filter(
        models.ProduitCatalogue.produit_nom == nom_produit.lower()
    ).first()

    if not produit_info:
        raise HTTPException(status_code=404, detail="Produit non trouvé au catalogue")

    # 2. ON CALCULE LE PRIX AUTOMATIQUEMENT (Exit le p_vente manuel !)
    # On utilise la logique de promo qu'on a vue juste avant
    prix_final = calculer_prix_automatique(nom_produit, db)

    # 3. On enregistre la vente avec le prix que L'IA a trouvé
    nouvelle_vente = models.Vente(
        produit_nom=nom_produit.lower(),
        quantite=quantite,
        prix_unitaire=prix_final, # C'est le prix calculé, pas saisi
        total_ligne=prix_final * quantite,
        entreprise_id=101, # Exemple
        date_heure=datetime.now()
    )
    
    # 4. TRÈS IMPORTANT : On baisse le stock automatiquement
    produit_info.stock_actuel -= quantite

    db.add(nouvelle_vente)
    db.refresh(nouvelle_vente)
    db.commit()
    
    return {"message": "Vente enregistrée", "prix_applique": prix_final,"ticket":nouvelle_vente.id}

    alerte = ""
    if stock.quantite_restante <= 5:
        alerte = f"⚠️ ATTENTION : Stock de {nom_produit.lower} presque épuisé ({stock.quantite_restante} restants) !"

    return {
        "status": "Vente réussie",
        "total_ligne": p_vente * qte,
        "alerte_stock": alerte
    }

@app.get("/caissier/verifier-promo/{nom_produit}")
def verifier_promo(nom_produit: str, db: Session = Depends(get_db)):
    maintenant = datetime.now()
    nom_clean = nom_produit.lower().strip()

    # On cherche une promo active pour ce produit
    promo = db.query(models.Promotion).filter(
        models.Promotion.produit_nom == nom_clean,
        models.Promotion.date_debut <= maintenant,
        models.Promotion.date_fin >= maintenant
    ).first()

    if promo:
        return {
            "en_promo": True,
            "message": f"🔥 PROMO : -{promo.reduction_pourcent}% ! {promo.message_promo}",
            "nouveau_prix_suggere": "Calculer selon le prix catalogue"
        }
    return {"en_promo": False}

@app.get("/caissier/generer-recu/{ticket}")
def generer_recu(ticket: str, db: Session = Depends(get_db)):
    ventes = db.query(models.Vente).filter(models.Vente.ticket_numero == ticket).all()
    if not ventes:
        raise HTTPException(status_code=404, detail="Ticket vide ou inconnu")
    
    total_ticket = sum([v.prix_vente * v.quantite for v in ventes])
    
    # Structure simplifiée du reçu pour l'impression
    lignes = [{"article": v.produit_nom, "qte": v.quantite, "prix": v.prix_vente} for v in ventes]
    
    return {
        "entete": "SUPERMARCHÉ SMART-AI",
        "ticket": ticket,
        "articles": lignes,
        "total": total_ticket,
        "conseil_ia": "N'oubliez pas les promotions au rayon " + ventes[0].categorie
    }



# --- ROUTES DE GESTION (Pour l'Admin) ---
@app.post("/admin/ajouter-produit-catalogue")
def ajouter_produit(nom: str, categorie: str, p_achat: float, stock_init: int, db: Session = Depends(get_db)):
    # On ajoute au catalogue + on initialise le stock
    nom_clean = nom.lower().strip()
    nouveau_p = models.ProduitCatalogue(nom=nom_clean, categorie=categorie, prix_achat=p_achat)
    nouveau_s = models.Stock(produit_nom=nom_clean, quantite_restante=stock_init)
    
    db.add(nouveau_p)
    db.add(nouveau_s)
    db.commit()
    return {"message": f"Produit {nom} prêt à la vente !"}


@app.post("/admin/creer-employe")
def creer_employe(username: str, password: str, entreprise_id: int, role: str, db: Session = Depends(get_db)):
    # 1. On vérifie si le nom existe déjà
    existe = db.query(models.User).filter(models.User.username == username).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ce nom d'utilisateur est déjà pris")
    pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
    #  CRYPTE mot de passe
    hashed_password = pwd_context.hash(password)

    # enregistre dans la base
    nouvel_user = models.User(
        username=username,
        password_hash=hashed_password,
        entreprise_id=entreprise_id,
        role=role # 'caissier' ou 'admin'
    )
    db.add(nouvel_user)
    db.commit()
    return {"message": f"Compte {role} créé avec succès pour {username} !"}

@app.post("/admin/creer-promotion")
def creer_promo(produit: str, pourcent: int, debut: str, fin: str, db: Session = Depends(get_db)):

    nouveau_debut = datetime.strptime(debut, "%Y-%m-%d")
    nouveau_fin = datetime.strptime(fin, "%Y-%m-%d")
    
    la_promo = models.Promotion(
        produit_nom=produit.lower(),
        reduction_pourcent=pourcent,
        date_debut=nouveau_debut,
        date_fin=nouveau_fin
    )
    db.add(la_promo)
    db.commit()
    return {"status": "Promotion enregistrée ! Elle s'activera automatiquement aux dates choisies."}

@app.post("/admin/maj-stock")
def mettre_a_jour_stock(nom: str, quantite_ajoutee: int, prix_achat: float, db: Session = Depends(get_db)):
    produit = db.query(models.ProduitCatalogue).filter(models.ProduitCatalogue.produit_nom == nom.lower()).first()
    
    if produit:
        produit.stock_actuel += quantite_ajoutee
        produit.prix_achat = prix_achat # On met à jour le prix d'achat si il a changé
        db.commit()
        return {"status": "Stock mis à jour"}
    
@app.get("/api/admin/all-data")
def get_all_data_for_ia(db: Session = Depends(get_db)):
    # On récupère les données de ton programme (Base de données)
    # Exemple avec tes tables SQL :
    ventes = db.query(models.Vente).all()
    stocks = db.query(models.Stock).all()
    clients = db.query(models.Vente).all()
    
    # On renvoie tout dans un seul gros dictionnaire
    return {
        "ventes": ventes,
        "stock": stocks,
        "clients": clients,
        "saison_actuelle": "Saison Sèche",
        "heure": 18
    }