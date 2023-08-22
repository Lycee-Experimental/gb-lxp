import sqlite3
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, PageBreak, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def df2table(df):
    """Fonction pour dessiner un tableau à partir d'un df"""
    df_tri = df[["Nom", "Prenom",'Telephone', "Situation", "Sexe","AECProjet"]].sort_values(by=['Situation','AECProjet'], ascending=False)
    return Table(
      [[Paragraph(col) for col in df_tri.columns]] + df_tri.values.tolist(), 
      style=[
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('LINEBELOW',(0,0), (-1,0), 1, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.lightgrey, colors.white]),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE')
        ],
      hAlign = 'LEFT',)


# Connection à la base de donnée
con = sqlite3.connect("base/base.db")
df = pd.read_sql("select * from Élèves", con)

# Definition du document PDF
doc = SimpleDocTemplate("output.pdf", pagesize=A4)

styles = getSampleStyleSheet() # Un raccourcis vers le style title

document = []
for gb in ['G1', 'G2','G3','G4','G5']:
    document.append(Paragraph(gb, styles['Title']))
    document.append(Spacer(1, 24))
    document.append(df2table(df[df["AECGroupeBase"]==gb]))
    document.append((PageBreak())
    )

# Création du document
doc.build(document)

