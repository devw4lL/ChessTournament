***********************************************************************************************************************
#                                                        **Chess Tournament**
## **Presentation:**

L'application Chass Tournament est une application de gestion de tournoi d'échec suivant le système suisse.
Cette application utilise une base de donnée géré par TinyDB, produisant un fichier db.json.


### **_utilisation_**

**--Créer un tournoi.**

Cette section vous permet de créer un nouveau tournoi.
Il vous sera également proposé la création de huit joueurs pour le tournoi.

**--Reprendre un tournoi.**

Cette section vous permet de reprendre un tournoi non fini à l'endroit
ou vous l'avez arrété la fois précédente.

**--Générer des rapports.**

---  Tout les joueurs par ordre alphabétique.            
---  Tout les joueurs par classement.                    
---  Tout les tournois.                                  
---  Tout les joeurs d\'un tournoi par odre alphabétique.
---  Tout les joeurs d\'un tournoi par classement.       
---  Tout les rounds d\'un tournoi.                      
---  Tout les matchs d\'un tournoi.                      
                                    
**--Gestion de la base de donnée.**

L'application utilise TinyDB pour la gestion de la base de donnée.

Vous pouvez trouver le fichier db.json dans le dossier ChessTournament/src/db/db.json.

Ce fichier peut être échanger entre ordinateur.

## **Requirement**

tinydb~=4.4.0

## **Windows install**

cd **/ChessTournament/

python -m venv venv

source /venv/Script/activate

pip install -r requirements.txt

python /ChessTounament/main.py

## **Unix install**

cd **/ChessTournament/

python -m venv venv

source /venv/bin/activate

pip install -r requirements.txt

python /ChessTounament/main.py

------------------------------------------------------------
### **Utilisation de Flake8**

##### **Installet Flake8 et son plugin de génération de rapport html:**

pip -install flake8 flake8_html

#### **Fichier de configuration:**

Le fichier setup.cfg à la racine du projet contient les configurations
demandés, cependant vous pouvez les modifier dans ce fichier.

#### **Générer un rpport:**

flake8 src --format=html --htmldir=flake8-rapport


