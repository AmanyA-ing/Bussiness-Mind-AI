import flet as ft
from ui.login import vue_login
from ui.caissier import vue_caissier
from ui.admin import vue_admin

def main(page: ft.Page):
    page.title = "Smart Retail IA"
    page.window_width = 1100
    page.window_height = 800

    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(ft.View("/", [vue_login(page)]))
        elif page.route == "/caissier":
            page.views.append(ft.View("/caissier", [
                ft.AppBar(title=ft.Text("Caisse"), bgcolor=ft.colors.SURFACE_VARIANT),
                vue_caissier(page)
            ]))
        elif page.route == "/admin":
            page.views.append(ft.View("/admin", [
                ft.AppBar(title=ft.Text("Admin Dashboard"), bgcolor=ft.colors.BLUE_700, color="white"),
                vue_admin(page)
            ]))
        page.update()

    page.on_route_change = route_change
    page.push_route("/")

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=9750)