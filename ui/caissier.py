import flet as ft
import requests
from ui.config import API_URL

def vue_caissier(page: ft.Page):
    panier = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    total_text = ft.Text("Total: 0 FCFA", size=30, weight="bold")
    
    input_nom = ft.TextField(label="Produit (ex: Riz)", expand=True)
    input_qte = ft.TextField(label="Qté", width=80, value="1")

    def ajouter(e):
        try:
            # Appel à l'API pour le prix auto + promo
            res = requests.get(f"{API_URL}/calculer-prix/{input_nom.value.lower()}")
            if res.status_code == 200:
                prix = res.json()["prix_final"]
                qte = int(input_qte.value)
                panier.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.SHOPPING_CART),
                        title=ft.Text(f"{input_nom.value.upper()} (x{qte})"),
                        subtitle=ft.Text(f"PU: {prix} FCFA | Total: {prix*qte} FCFA")
                    )
                )
                # Update total (logique simple)
                page.update()
        except:
            page.snack_bar = ft.SnackBar(ft.Text("Erreur: Produit inconnu"))
            page.snack_bar.open = True
            page.update()

    return ft.Container(
        content=ft.Column([
            ft.Text("Terminal Caisse", size=20, weight="bold"),
            ft.Row([input_nom, input_qte, ft.IconButton(ft.icons.ADD_CIRCLE, on_click=ajouter, icon_color="green")]),
            ft.Divider(),
            panier,
            ft.Divider(),
            ft.Row([total_text, ft.ElevatedButton("VALIDER & IMPRIMER", bgcolor="green", color="white")], alignment="spaceBetween")
        ]), padding=20, expand=True
    )