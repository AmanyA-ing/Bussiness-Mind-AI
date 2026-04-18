from fpdf import FPDF
from database import SessionLocal
import models

def generer_rapport_mensuel(entreprise_id,donnees_historiques):
    try:
        if not donnees_historiques or len(donnees_historiques) < 2:
            return 0 # Retourne 0 au lieu de faire planter l'app
            
    except Exception as e:
        print(f"Erreur IA : {e}")
        return 0
    
    db = SessionLocal()
    # On récupère toutes les ventes du mois pour cette boutique
    ventes = db.query(models.Vente).filter(models.Vente.entreprise_id == entreprise_id).all()
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    
    # En-tête
    pdf.cell(200, 10, txt=f"RAPPORT FINANCIER - BOUTIQUE #{entreprise_id}", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)

    # Chiffres clés (Calculés via la DB)
    total_ca = sum([v.prix_vente * v.quantite for v in ventes])
    total_benef = sum([v.benefice_total for v in ventes])
    
    pdf.cell(200, 10, txt=f"Chiffre d'Affaires Total : {total_ca} FCFA", ln=True)
    pdf.cell(200, 10, txt=f"Bénéfice Net : {total_benef} FCFA", ln=True)
    pdf.ln(5)
    
    # Tableau des ventes
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(60, 10, "Article", 1, 0, 'C', True)
    pdf.cell(40, 10, "Quantité", 1, 0, 'C', True)
    pdf.cell(50, 10, "Total", 1, 1, 'C', True)

    for v in ventes:
        pdf.cell(60, 10, v.produit_nom, 1)
        pdf.cell(40, 10, str(v.quantite), 1)
        pdf.cell(50, 10, f"{v.prix_vente * v.quantite}", 1, 1)

    nom_fichier = f"rapport_mensuel_{entreprise_id}.pdf"
    pdf.output(nom_fichier)
    return nom_fichier