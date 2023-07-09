import sqlite3
import pandas as pd

con = sqlite3.connect("/home/davy/base.db")
df = pd.read_sql("select * from Élèves", con)

# Formate les nom avec des majuscules au début
df["Nom"]=df["Nom"].str.title()
df["Prenom"]=df["Prenom"].str.title()
df["Responsable1Nom"]=df["Responsable1Nom"].str.title()
df["Responsable2Nom"]=df["Responsable2Nom"].str.title()

# Formate les numéros de téléphone avec des espaces
def format_phone_number(number):
    if number is None:
        return ''
    digits_only = ''.join(filter(str.isdigit, number))
    formatted_number = ' '.join([digits_only[i:i+2] for i in range(0, len(digits_only), 2)])
    return formatted_number
df['Telephone'] = df['Telephone'].apply(lambda x: format_phone_number(x))
df['Responsable1Telephone'] = df['Responsable1Telephone'].apply(lambda x: format_phone_number(x))
df['Responsable2Telephone'] = df['Responsable2Telephone'].apply(lambda x: format_phone_number(x))

# Définition des variables
gbs = ['G1', 'G2', 'G3', 'G4', 'G5']
anciennetes = ['Ancien·ne', "Nouvelleau"]
genres = ["M","F","A"]
niveaux = [ "Terminale", "CREPA", "Déter", "Première"]
spe1 = ['ArtPla', 'Ciné', 'Théatre', 'HGGSP'] 
spe2 = ['Anglais', 'Espagnol', 'SVT', 'Maths']
spe3 = ['SES', 'HLP', 'NSI', 'PhyChim']
mee = {
'Nath': 'G4',
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
df.to_sql("Élèves", con, if_exists="replace", index=False, dtype={'ID': 'INTEGER PRIMARY KEY AUTOINCREMENT'})
con.close()

