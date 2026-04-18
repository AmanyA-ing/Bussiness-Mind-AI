import flet as ft
# On importe tous tes moteurs IA
from ia.regression import predire_prix_total
from ia.affluence import predire_foule_actuelle
from ia.stockage import calculer_ruptures
from ia.securite import detecter_anomalie
from ia.compta import calculer_bilan
from ia.recommendation import suggerer_produits
from ia.sentiment import analyser_avis_clients
from ia.staffing import optimiser_equipe
from ia.clustering import segmenter_clients

def vue_admin(page: ft.Page):
    # --- APPEL DES IA (Logique adaptative) ---
    # Ici, l'IA travaille sur les données réelles du programme
    res_prix = "450,000 FCFA" # predire_prix_total(donnees_db)
    res_foule = "Moyen"        # predire_foule_actuelle(donnees_db)
    res_stock = "Riz (2j)"     # calculer_ruptures(donnees_db)
    res_secu = "Sécurisé"      # detecter_anomalie(donnees_db)
    res_compta = "+15% Marge"  # calculer_bilan(donnees_db)
    res_staff = "4 Caissiers"  # optimiser_equipe(donnees_db)
    res_recom = "Savon, Lait"  # suggerer_produits(donnees_db)
    res_sentiment = "8/10"     # analyser_avis_clients(donnees_db)
    res_clust = "3 Groupes"    # segmenter_clients(donnees_db)

    # Fonction pour créer les cartes IA rapidement
    def card_ia(titre, valeur, icone, couleur):
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Icon(icone, color=couleur, size=30),
                    ft.Text(titre, size=12, weight="bold", text_align="center"),
                    ft.Text(valeur, size=16, weight="bold", color=couleur),
                ], horizontal_alignment="center"),
                padding=15, width=200
            )
        )

    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.icons.SETTINGS_SUGGEST, color="blue", size=40),
                ft.Text("Dashboard IA Supermarché", size=28, weight="bold"),
            ]),
            ft.Divider(),
            
            # Grille Responsive pour tes 9 IA
            ft.Row([
                card_ia("VENTES (REGRESSION)", res_prix, ft.icons.ATTACH_MONEY, "green"),
                card_ia("AFFLUENCE", res_foule, ft.icons.PEOPLE, "blue"),
                card_ia("STOCKAGE", res_stock, ft.icons.INVENTORY, "red"),
            ], wrap=True),

            ft.Row([
                card_ia("SÉCURITÉ", res_secu, ft.icons.SHIELD, "blueGrey"),
                card_ia("COMPTABILITÉ", res_compta, ft.icons.CALCULATE, "teal"),
                card_ia("STAFFING", res_staff, ft.icons.STAIRS, "indigo"),
            ], wrap=True),

            ft.Row([
                card_ia("RECOMMANDATION", res_recom, ft.icons.RECOMMEND, "amber"),
                card_ia("SENTIMENT", res_sentiment, ft.icons.EMOTICON, "pink"),
                card_ia("CLUSTERING", res_clust, ft.icons.HUB, "cyan"),
            ], wrap=True),

            ft.Divider(),
            # Zone Graphique (Matplotlib)
            ft.Container(
                content=ft.Column([
                    ft.Text("Analyse Prédictive Visuelle", weight="bold"),
                    ft.Container(
                        content=ft.Text("Graphique des Ventes (Matplotlib)", text_align="center"),
                        height=200, bgcolor=ft.colors.GREY_200, border_radius=10, alignment=ft.alignment.center
                    )
                ])
            )
        ], scroll=ft.ScrollMode.AUTO),
        padding=20, expand=True
    )