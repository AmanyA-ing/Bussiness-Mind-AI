import flet as ft

def vue_login(page: ft.Page):
    user_input = ft.TextField(label="Utilisateur", width=300, prefix_icon=ft.icons.PERSON)
    pass_input = ft.TextField(label="Mot de passe", password=True, can_reveal_password=True, width=300)

    def valider(e):
        if user_input.value == "admin":
            page.session.set("role", "admin")
            page.go("/admin")
        else:
            page.session.set("role", "caissier")
            page.go("/caissier")

    return ft.Container(
        content=ft.Column([
            ft.Icon(ft.icons.LOCK_PERSON, size=60, color="blue"),
            ft.Text("Smart Retail Login", size=25, weight="bold"),
            user_input,
            pass_input,
            ft.ElevatedButton("Se Connecter", on_click=valider, width=200)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        alignment=ft.alignment.center, expand=True
    )