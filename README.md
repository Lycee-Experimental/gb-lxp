# GB-LXP

Une base élève vierge basée sur libreoffice Base (`libreoffice-base.odb`) et SQLite (`base-sample.db`), et un script pour générer les groupes de base (`script_sql.py`).

## Utilisation d'une base SQLite3
Pour pouvoir interfacer la base plus facilement avec python, il faut externaliser les données (car elles sont par défaut intégrées au fichier `.odb`).
Pour éviter d'avoir à mettre en place une base MySql ou Posgresql, nous allons simplement utiliser une base **SQLite** qui tient dans un fichier que nous nommerons `base.db`.

### Installation de ODBC
**ODBC** est le protocole qui permettra de faire le lien entre Libreoffice et la base **SQLite**.
```bash
sudo apt install unixodbc-common libsqliteodbc
```
### Configuration de ODBC

Après installation le fichier `/etc/odbcinst.ini` devrait avoir le contenu suivant :

```ini
[SQLite]
Description=SQLite ODBC Driver
Driver=libsqliteodbc.so
Setup=libsqliteodbc.so
UsageCount=1

[SQLite3]
Description=SQLite3 ODBC Driver
Driver=libsqlite3odbc.so
Setup=libsqlite3odbc.so
UsageCount=1
```

Il faut ensuite renseigner la destination de notre base élève.

```bash
sudo nano /etc/odbc.ini 
```

```ini
[BaseEleve]
Description= Base élève du LXP
Driver= SQLite3
Database= ... à compléter avec la destination de la db ...
Timeout= 1000
StepAPI= No
```

## Passage au Dark Mode :

> outils > options > Libre Office 

> Affichage > Mode : sombre, Thème : Colibre(SVG+Dark)

> Couleur de l'interface : Libreoffice Dark

## Ouvrir le formulaire au démarage de base

### Permettre l'éxécution de macros

Sécurité > Sécurité des macros > Faible

### Création d'une macro

Macro :
Outils > MAcro > Gérer les macros > Basic > Nouveau 

```basic
SUB OuvrirFormulaire
  Dim ObjTypeWhat
  Dim ObjName As String
  ObjName = "FichesEleve"
  ObjTypeWhat = com.sun.star.sdb.application.DatabaseObject.FORM
  If ThisDatabaseDocument.FormDocuments.hasbyname(ObjName) Then 'Check the form exists'
      With Thisdatabasedocument.currentcontroller
        If  Not .isConnected Then .connect
      End With
     ThisDatabaseDocument.CurrentController.loadComponent(ObjTypeWhat, ObjName, FALSE) 'Open the form'
  Else
      MsgBox "Error! Wrong form name used. " & ObjName
  End if
End Sub
```

### Lancement de la macro à l'ouverture d'un doc

Outils > Personaliser > Ouvrir le document > Macro... et sélectionner la macro configurée précédement.


