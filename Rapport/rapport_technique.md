# Rapport Technique : Fonctionnement de l'Application de Trading

## Introduction
Ce rapport technique explique le fonctionnement de l'application de trading construite avec la plateforme Ingescape, reposant sur plusieurs agents qui interagissent pour effectuer des opérations de trading simulées. Chaque agent joue un rôle spécifique et communique avec les autres via des services, afin de gérer les ordres de trading, le solde des comptes, les graphiques financiers et les informations partagées sur le Whiteboard.

## Structure Globale de l'Application
L'application de trading est composée de plusieurs agents qui travaillent ensemble de manière coordonnée. Chaque agent exécute des tâches spécifiques et est responsable de certaines fonctionnalités de l'application.

Les agents de l'application sont :
- **Banque**
- **Graphique**
- **Trader Manuel**
- **Trader**
- **Whiteboard**

Chacun de ces agents sera présenté en détail dans les sections suivantes.

## Agent : Banque
### Fonctionnalités
L'agent **Banque** est responsable de la gestion financière de l'application. Il gère les comptes des traders, les quantitsés de jetons disponibles et le prix des jetons. La banque est également chargée de maintenir un historique des transactions.

### Services Implémentés
- **creation_compte** : Crée un compte pour un trader qui n'en possède pas encore.
- **get_info_compte** : Fournit des informations sur le solde et les jetons d'un compte existant.
- **ordre** : Traite les ordres de trading (achat ou vente de jetons) -> Une sécurité a été ajouté pour ne passer un ordre que si le compte existe dans la banque. S'il n'existe pas alors on en créé un pour l'agent concerné.

### Fonctionnalités Clés
- **Gestion des Comptes** : Lorsqu'un trader fait une demande d'achat ou de vente, l'agent Banque crée un compte pour ce trader s'il n'en possède pas déjà.
- **Mise à Jour des Prix** : Le prix des jetons est ajusté en fonction des transactions effectuées.
- **Historique des Ordres** : L'historique des transactions est affiché sur le Whiteboard, montrant les 5 derniers ordres.

## Agent : Graphique
### Fonctionnalités
L'agent **Graphique** est chargé de générer et de mettre à jour les graphiques financiers à partir des données de trading collectées. Ces graphiques sont ensuite envoyés au Whiteboard pour être affichés visuellement.

### Services Implémentés
- **mettre_a_jour_graphique** : Crée un graphique des prix sous forme de chandeliers à partir des données récentes.
- **creer_image_interface_trading** : Crée une interface graphique de trading statique pour donner une présentation visuelle de l'application.

### Fonctionnalités Clés
- **Génération Continue de Graphiques** : Utilise des threads pour collecter les données de trading et générer des graphiques actualisés, qui sont envoyés sur le Whiteboard à des intervalles réguliers.
- **Interface Visuelle de Trading** : Fournit une interface de trading pour le Whiteboard, améliorant la compréhension visuelle des opérations par les utilisateurs.

## Agent : Trader Manuel
### Fonctionnalités
L'agent **Trader Manuel** est une interface utilisateur qui permet aux utilisateurs de créer des comptes de trading et de passer des ordres d'achat et de vente. Cet agent utilise une interface graphique (GUI) écrite avec Tkinter.

### Services Implémentés
- **creer_compte** : Permet à l'utilisateur de créer un compte de trader.
- **acheter** et **vendre** : Envoient des ordres à la Banque pour acheter ou vendre des jetons.

### Fonctionnalités Clés
- **Interface Utilisateur Graphique** : Utilise Tkinter pour permettre aux utilisateurs d'intéragir avec le système de trading, créer des comptes et passer des ordres.
- **Interactions avec la Banque** : Fait des appels à l'agent Banque pour les opérations financières et met à jour les soldes et jetons en fonction des transactions.

## Agent : Trader
### Fonctionnalités
L'agent **Trader** agit de manière autonome et gère des transactions aléatoirement (achat/vente/quantité aléatoire). Il peut également interagir avec l'agent Banque pour acheter ou vendre des jetons.

### Fonctionnalités Clés
- **Stratégies Automatisées** : Gère des ordres d'achat et de vente.
- **Communication avec la Banque** : L'agent Trader envoie des demandes de transaction à l'agent Banque pour les éxecuter.

## Agent : Whiteboard
### Fonctionnalités
Le **Whiteboard** est un espace de visualisation centralisé, utilisé pour afficher les graphiques financiers, l'historique des ordres et d'autres éléments visuels pertinents pour le trading. Il est mis à jour par différents agents.

### Fonctionnalités Clés
- **Affichage des Graphiques** : Reçoit des graphiques de l'agent Graphique et les affiche.
- **Historique des Ordres** : Affiche l'historique des ordres émis, mis à jour par l'agent Banque.
- **Gestion des Éléments avec Threads** : Utilise une stratégie multi-threading pour assurer que les mises à jour d'affichage ne provoquent pas de superposition ou d'erreurs visuelles.

## Communication Entre les Agents
La communication entre les agents est basée sur un mécanisme de services appelé "service-call" de la plateforme Ingescape. Chaque agent expose certains services que les autres agents peuvent appeler en fonction de leurs besoins.
- **Banque et Whiteboard** : L'agent Banque met à jour l'historique des ordres sur le Whiteboard pour afficher les dernières transactions.
- **Graphique et Whiteboard** : L'agent Graphique génère régulièrement des graphiques financiers qui sont publiés sur le Whiteboard.
- **Trader Manuel et Banque** : Trader Manuel interagit avec l'agent Banque pour créer des comptes et passer des ordres.

## Synchronisation et Threads
L'application utilise des threads pour gérer différents aspects, garantissant une fluidité dans l'affichage et la gestion des données en temps réel.
- **Thread de Mise à Jour du Whiteboard** : Utilisé pour supprimer les anciens éléments du Whiteboard avant d'en ajouter de nouveaux.
- **Thread de Mise à Jour du Prix** : L'agent Banque utilise un thread pour ajuster constamment le prix des jetons en fonction des transactions.
- **Thread de Génération des Graphiques** : L'agent Graphique utilise un thread pour collecter les données et générer des graphiques toutes les secondes.

## Conclusion
Ce rapport a présenté les différents agents qui composent l'application de trading, ainsi que leurs rôles, leurs services, et leurs communications. Chaque agent est une partie essentielle du système global et communique avec les autres agents à travers les services fournis par la plateforme Ingescape. L'application repose sur une synchronisation à l'aide de threads pour garantir la cohérence des informations affichées sur le Whiteboard et la réactivité de l'application pour l'utilisateur.

Les futures améliorations pourraient inclure une meilleure gestion de la synchronisation pour éviter les superpositions sur le Whiteboard, ainsi que des fonctionnalités sur l'interface du trader manuel pour une meilleure expérience utilisateur. On pourait aussi ajouter de vraie stratégie pour les agents trader automatique et définir le prix actuel de l'actif avec de vraie calculs et non seulement en fonction du nombre de jetons disponibles.
