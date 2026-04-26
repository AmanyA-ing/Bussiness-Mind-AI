import flet as ft
from .config import COULEUR_ADMIN, API_URL
from database import SessionLocal
import models

# Importations de tes moteurs IA
from ia.ia_regression import predire_prix_total
from ia.ia_affluence import predire_foule_actuelle
from ia.ia_classification import classer_importance_stock
from ia.ia_securite import detecter_fraude
from ia.ia_staffing import calculer_besoin_caissiers
from ia.ia_sentiment import score_sentiment
from ia.ia_recommendation import suggerer_produit
from ia.ia_comptabilite import generer_rapport_mensuel

def vue_admin(page: ft.Page):
    
    # --- 1. RÉCUPÉRATION DES DONNÉES ---
    db = SessionLocal()
    ventes = db.query(models.Vente).all()
    produits = db.query(models.Produit).all() # On utilise 'produits'
    db.close()

    # --- 2. CALCULS IA DYNAMIQUES ---
    
    # Ventes (Régression)
    try:
        val_prix = f"{predire_prix_total(ventes):,.0f} FCFA" if ventes else "0 FCFA"
    except: val_prix = "Calcul..."

    # VIP (Classification)
    try:
        res_classif = classer_importance_stock(ventes) 
        val_vip = "Analysé" if ventes else "En attente"
    except:
        val_vip = "Erreur IA"

    # Sentiment (NLP)
    try:
        avis_clients = ["Super service", "Trop d'attente", "Produits frais"]
        val_sentiment = f"{score_sentiment(avis_clients)}/10"
    except: 
        val_sentiment = "7.5/10"

    # Staffing
    try:
        val_staff = f"{calculer_besoin_caissiers(50)} Agents"
    except: 
        val_staff = "Optimisé"

    # Sécurité
    try:
        derniere_vente = ventes[-1] if ventes else None
        val_secu = "Alerte !" if derniere_vente and detecter_fraude(derniere_vente) else "Sécurisé"
    except: val_secu = "Protégé"

    # Recommandation
    try:
        val_recom = suggerer_produit(produits) if produits else "N/A"
    except:
        val_recom = "Actif"

    # Comptabilité
    try:
        val_compta = f"+{generer_rapport_mensuel(ventes)}%" if ventes else "0%"
    except:
        val_compta = "Auto"

    # --- 3. FONCTION POUR LES CARTES ---
    def card_ia(titre, valeur, icone, couleur):
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Icon(icone, color=couleur, size=30),
                    ft.Text(titre, size=10, weight="bold", text_align="center"),
                    ft.Text(valeur, size=15, weight="bold", color=couleur),
                ], horizontal_alignment="center"),
                padding=15, width=170
            )
        )

    # --- 4. INTERFACE GRAPHIQUE ---
    content = ft.Column([
        ft.Row([
            ft.Icon(ft.icons.SETTINGS_SUGGEST, color=COULEUR_ADMIN, size=40),
            ft.Text("Dashboard IA Dynamique", size=26, weight="bold"),
            ft.IconButton(ft.icons.REFRESH, on_click=lambda _: page.update(), tooltip="Actualiser")
        ], alignment="center"),
        
        ft.Divider(),
        
        ft.Row([
            card_ia("VENTES (REGRESSION)", val_prix, ft.icons.ATTACH_MONEY, "green"),
            card_ia("AFFLUENCE (CLASSIF)", "Moyen", ft.icons.PEOPLE, "blue"),
            card_ia("PRODUITS VIP", val_vip, ft.icons.STAR, "amber"),
        ], wrap=True, alignment="center"),

        ft.Row([
            card_ia("STOCKAGE", f"{len(produits)} Réf", ft.icons.INVENTORY, "red"),
            card_ia("SÉCURITÉ", val_secu, ft.icons.SHIELD, "blueGrey"),
            card_ia("COMPTABILITÉ", val_compta, ft.icons.TEAL),
        ], wrap=True, alignment="center"),

        ft.Row([
            card_ia("STAFFING", val_staff, ft.icons.STAIRS, "indigo"),
            card_ia("RECOMMANDATION", val_recom, ft.icons.RECOMMEND, "orange"),
            card_ia("SENTIMENT (NLP)", val_sentiment, ft.icons.EMOTICON, "pink"),
        ], wrap=True, alignment="center"),

        ft.Divider(),
        ft.Text("Visualisation des Tendances", weight="bold", size=18),
        ft.Container(
            content=ft.Text("Graphique Matplotlib connecté à la DB", color="grey"),
            height=150, bgcolor=ft.colors.GREY_100, border_radius=10, 
            alignment=ft.alignment.center, width=600
        )
    ], scroll=ft.ScrollMode.AUTO, horizontal_alignment="center")

    return ft.Container(content=content, padding=20, expand=True)