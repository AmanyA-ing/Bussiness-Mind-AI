from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

# 1. UTILISATEURS (Qui se connecte ?)
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    entreprise_id = Column(Integer)
    username = Column(String, unique=True)
    password_hash = Column(String)
    role = Column(String) # 'admin' pour le Boss, 'caissier' pour l'employé

# 2. VENTES (Le cœur du système)
class Vente(Base):
    __tablename__ = "ventes"
    id = Column(Integer, primary_key=True, index=True)
    
    # Identifiants de transaction
    entreprise_id = Column(Integer)

    # Données brutes
    produit_nom = Column(String)
    categorie = Column(String) # Ex: Alimentation, Beauté, Boisson
    
    prix_vente = Column(Float)
    quantite = Column(Integer)
    
    caissier_nom = Column(String)

    date_heure = Column(DateTime, default=datetime.now)
    moment_journee = Column(String) # Matin / Midi / Soir / Nuit
    saison = Column(String)     # Saison des pluies / Saison sèche
    date=Column(String, default=datetime.now)
    benefice_total = Column(Float)
    
    # Données pour l'IA (Analyse de sentiments)
    commentaire_client = Column(Text, nullable=True)
    sentiment_score = Column(Float, default=0.0) # Score de -1 à 1


class ProduitCatalogue(Base):
    __tablename__ = "catalogue"
    id = Column(Integer, primary_key=True)
    produit_nom = Column(String, unique=True, index=True)
    prix_achat = Column(Float)
    prix_vente_base = Column(Float)
    stock_actuel = Column(Integer)

class Promotion(Base):
    __tablename__ = "promotions"
    id = Column(Integer, primary_key=True, index=True)
    produit_nom = Column(String)
    reduction_pourcent = Column(Integer) 
    date_debut = Column(DateTime)
    date_fin = Column(DateTime)
    message_promo = Column(String)
    
# 3. STOCK (Pour les alertes de rupture)
class Stock(Base):
    __tablename__ = "stocks"
    id = Column(Integer, primary_key=True, index=True)
    produit_nom = Column(String, unique=True)
    quantite_actuelle = Column(Integer)
    seuil_alerte = Column(Integer, default=10) 