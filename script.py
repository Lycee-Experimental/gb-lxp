import pandas as pd
from openpyxl import load_workbook

## G1 : pas esp, pas maths, pas théatre (3)
## G2 : pas NSI/PC / pas HLP / pas philo (1 & 2)
## G3 : pas SVT / HLP (1)
## G4 : pas SES / HGGSP / Ciné (2)
## G5 : pas AMC/Art (3)
## Elève qui lâche la 1 -> G3 (G2)
## Elève qui lache la 2 -> G4 (G2)
## Elève qui lache la 3 -> G5 ou G1

# Ouverture du fichier excel
file_path = "base/base-eleve2.xlsx"
df = pd.read_excel(file_path)

gbs = ['G1', 'G2', 'G3', 'G4', 'G5']
anciennetes = ['Ancien·ne', "Nouvelleau"]
genres = ["M","F","A"]
niveaux = [ "Terminale", "CREPA", "Déter", "Première"]
spe1 = ['ArtPla', 'Ciné', 'Théatre', 'HGGSP'] 
spe2 = ['Anglais', 'Espagnol', 'SVT', 'Maths']
spe3 = ['SES', 'HLP', 'NSI', 'PhyChim']
mee = {
'Nath': 'G1',
'Clem': 'G2',
'Benj': 'G4',
'Julie': 'G3',
'Valentin': 'G5',
'Davy': 'G2',
'Maria': 'G3',
'Maude': 'G5',
'Fanny': 'G5',
'Enoch': 'G1',
'Mika': 'G3',
'Flora': 'G4',
'Renaud':'G4'
}

for niveau in niveaux:
    for genre in genres:
        for anciennete in anciennetes:
            selected_rows = df[(df["Ancienneté"] == anciennete) & (df["Genre"] == genre) & (df["Niveau"] == niveau)].sample(frac=1)
            for index, row in selected_rows.iterrows():  
                value_counts = df["GB"].value_counts()
                
                print(value_counts)
                if niveau == 'Terminale':        
                    spes = row[['spe1', 'spe2', 'spe3']].values
                    combi_spe = []
                    for spe in spe1:
                        if spe in spes:
                            combi_spe.append(1)
                    for spe in spe2:
                        if spe in spes:
                            combi_spe.append(2)
                    for spe in spe3:
                        if spe in spes:
                            combi_spe.append(3)
                    if 1 not in combi_spe:
                        result = ['G3','G2']
                    if 2 not in combi_spe:
                        result = ['G4','G2']
                    if 3 not in combi_spe:
                        result = ['G5','G1']
                    
                    if pd.notna(row[['ECCO']].values):
                        ecco = row[['ECCO']].values
                        result = [value for value in result if value != mee[ecco[0]]]
                    print(result)
                    sorted_result = sorted(result, key=lambda x: value_counts.get(x, 0))
                    print(sorted_result[0])
                    df.loc[index, 'GB'] = sorted_result[0]
                else:
                    if pd.notna(row[['ECCO']].values):
                        ecco = row[['ECCO']].values
                        result = [value for value in gbs if value != mee[ecco[0]]]
                    else:
                        result = gbs
                    print(result)
                    sorted_result = sorted(result, key=lambda x: value_counts.get(x, 0))
                    print(sorted_result)
                    df.loc[index, "GB"] = sorted_result[0]


# Enregistrement
writer = pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace')
writer.book = load_workbook(file_path)
#writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)
df.to_excel(writer, index=False)
writer.save()
