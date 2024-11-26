# UPSSI-Trading

## Description
UPSSI-Trading est une application de trading simulée utilisant une interface graphique (Whiteboard) pour visualiser l'évolution des prix et gérer des ordres de trading en temps réel. L'application permet de créer des comptes de traders, d'effectuer des transactions d'achat et de vente, et de mettre à jour l'historique des ordres sur le Whiteboard.

### Rapport sur le fonctionnement : [rapport technique](./Rapport/rapport_technique.md)

### Démonstration vidéo : https://youtu.be/QI6BDmu1vII

## Fonctionnalités
- Création de comptes de trading.
- Gestion des ordres d'achat et de vente.
- Interface graphique pour l'affichage des données de trading.
- Historique des transactions mis à jour en temps réel.

## Installation
1. **Clonez le dépôt** :
    ```bash
    git clone https://github.com/pierredaudin/Trading-platform.git
    cd Trading-platform
    ```
2. **Installez les dépendances** :
    ```bash
    pip install -r requirements.txt
    ```
3. **Lancer l'application** :
    ```bash
    python lanceur_trading.py
    ```

## Utilisation
- Pour démarrer l'application, lancez le script `lanceur_trading.py`.
- Suivez les instructions pour choisir les exécutables et les fichiers requis (executable ingescape).
- L'interface de trading s'affichera, et vous pourrez interagir avec les différentes fonctionnalités.
- Mettez le Whiteboard en plein écran et ouvrez le fenêtre du trader manuel

## Structure du Projet
- **lanceur_trading.py** : Script pour démarrer tous les services nécessaires (Whiteboard, Banque, Graphique, etc.).
- **Graphique/** : Contient le code pour générer et mettre à jour les graphiques du trading.
- **Banque/** : Contient la logique de gestion des comptes et des ordres des traders.
- **Trader_Manuel/**, **Trader_1/**, **Trader_2/**, **Trader_3/**, **Trader_4/**,**Trader_5/** : Différents agents de trading avec leurs interfaces respectives.

## Test V&V
Nous avons essayé de réaliser les tests, mais nous avons eu de nombreuses difficultés car nos agents dépendent les uns des autres et les valeurs à tester pour chaque agent (comme le solde d'un trader ou si un solde est créé) n'ont pas été implémentées de façon à ce qu'on puisse y avoir accès facilement.
Par exemple, si on crée un compte, il faut avoir l'association entre le numéro UUID et le nom de l'agent, puis afficher les comptes créés.
Uniquement pour tester une partie d'un service, il faudrait faire des modifications dans deux agents, afin d'avoir un aspect visuel ou un retour de ces informations.

Cela nous a emmenés à la conclusion que faire ces tests pour tous nos services nous demanderait encore plusieurs heures de travail supplémentaires. Nous avons quand même laissé un fichier de test, mais il ne fonctionne pas.

## Licence
[MIT License](LICENSE)
