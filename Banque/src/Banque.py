#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  Banque.py
#  Banque
#  Created by Ingenuity i/o on 2024/11/22
#
# "no description"
#
import ingescape as igs
import threading
import time
from datetime import datetime
import queue

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Banque(metaclass=Singleton):
    def __init__(self):
        self.jetons = 1000  # Quantité initiale de jetons que la banque possède
        self._prix = 10.0  # Prix initial des jetons (doit être un float)
        self.comptes = {}  # Dictionnaire pour gérer les comptes des traders
        self.stop_thread = False
        self.update_thread = threading.Thread(target=self.update_price_continuously)
        self.update_thread.start()
        self.ordre_historique = [] # Liste pour garder l'historique des ordres
        self.last_y_position = 100  # Position Y initiale pour éviter les superpositions
        self.elements_list = {}
        self.ordre_tokens = []  # Liste limitée à 5 éléments max

        # File d'attente pour la suppression des éléments du Whiteboard
        self.remove_queue = queue.Queue() 
        self.remove_thread = threading.Thread(target=self.process_remove_queue)
        self.remove_thread.daemon = True
        self.remove_thread.start()
        self.lock = threading.Lock()  # Verrou pour la gestion des mises à jour du Whiteboard

    # outputs
    @property
    def prix_actuelO(self):
        return self._prix

    @prix_actuelO.setter
    def prix_actuelO(self, value):
        self._prix = value
        if self._prix is not None:
            igs.output_set_double("prix_actuel", self._prix)
            #print(f"Prix actuel mis à jour : {self._prix} euros")

    # services
    def creation_compte(self, sender_agent_name, sender_agent_uuid, nom):
        self.creer_compte(sender_agent_uuid)

    def get_info_compte(self, sender_agent_name, sender_agent_uuid):
        if sender_agent_uuid in self.comptes:
            compte = self.comptes[sender_agent_uuid]
            solde = compte["argent"]
            jetons = compte["jetons"]
            igs.service_call(sender_agent_name, "reponse_info_compte", (solde, jetons), "")
        else:
            print(f"Le compte du trader {sender_agent_name} n'existe pas.")

    def ordre(self, sender_agent_name, sender_agent_uuid, quantite, type_ordre):
        # Vérifier si le trader a un compte, sinon en créer un
        if sender_agent_uuid not in self.comptes:
            self.creer_compte(sender_agent_uuid)
            print(f"Compte créé pour le trader {sender_agent_name} ({sender_agent_uuid})")
        
        # Récupérer le compte du trader
        compte = self.comptes[sender_agent_uuid]
        
        # Afficher les détails de l'ordre reçu
        print(f"Banque reçoit un ordre de {sender_agent_name} pour {type_ordre} {quantite} jetons.")
        
        # Traiter l'ordre reçu d'un trader, achat ou vente
        if type_ordre == "acheter":
            self.acheter(sender_agent_name, quantite, compte)
        elif type_ordre == "vendre":
            self.vendre(sender_agent_name, quantite, compte)

        # Ajouter l'ordre à l'historique
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.ordre_historique.append((sender_agent_name, type_ordre, quantite, timestamp))

        # Mettre à jour le prix et l'historique sur le Whiteboard
        self.mettre_a_jour_prix()
        self.prix_actuelO = self._prix

        # Mettre a jour le whiteboard 
        self.mettre_a_jour_whiteboard()


    def creer_compte(self, trader_uuid):
        # Créer un compte avec un solde initial
        self.comptes[trader_uuid] = {"argent": 1000.0, "jetons": 0}

    def acheter(self, agent_name, quantite, compte):
        if compte["argent"] >= quantite * self._prix and self.jetons >= quantite:
            compte["argent"] -= quantite * self._prix
            compte["jetons"] += quantite
            self.jetons -= quantite
            print(f"{agent_name} a acheté {quantite} jetons à {self._prix} euros chacun.")
        else:
            print(f"Achat refusé : {agent_name} n'a pas assez d'argent ou la banque n'a pas assez de jetons.")

    def vendre(self, agent_name, quantite, compte):
        if compte["jetons"] >= quantite:
            compte["jetons"] -= quantite
            compte["argent"] += quantite * self._prix
            self.jetons += quantite
            print(f"{agent_name} a vendu {quantite} jetons à {self._prix} euros chacun.")
        else:
            print(f"Vente refusée : {agent_name} n'a pas assez de jetons pour vendre {quantite} jetons.")

    def mettre_a_jour_prix(self):
        # Mettre à jour le prix en fonction du nombre de jetons disponibles (avec des valeurs en float)
        self._prix = 10.0 + (1000 - self.jetons) * 0.01

    """ def mettre_a_jour_whiteboard(self):
        try:
            # Ajouter un titre pour l'historique
            titre = "Historique des 5 derniers ordres"
            igs.service_call("Whiteboard", "addText", (titre, 50.0, 485.0, "#000000"), "")

            # Réafficher les 5 derniers ordres de l'historique
            derniers_ordres = self.ordre_historique[-5:]  # Ne garder que les 5 derniers
            y_position = 550.0  # Position initiale sur l'axe Y pour l'affichage des ordres (doit être un float)

            for ordre in derniers_ordres:
                trader_name, type_ordre, quantite, timestamp = ordre
                texte = f"{timestamp} - {trader_name} - {type_ordre} : {quantite} jetons"

                # Ajouter un rectangle pour "effacer" l'ancienne ligne de texte
                largeur_rectangle = 1000.0  # Largeur du rectangle pour couvrir tout le texte
                hauteur_rectangle = 75.0  # Hauteur du rectangle (ajustée pour couvrir une ligne de texte)
                x_position_rectangle = 40.0  # Position X du rectangle
                y_position_rectangle = y_position - 20.0  # Ajuster légèrement la position pour couvrir l'ancienne ligne
                couleur_fond = "#FFFFFF"  # Couleur de fond du Whiteboard (ajuster selon la couleur du fond)

                igs.service_call("Whiteboard", "addShape", ("rectangle", x_position_rectangle, y_position_rectangle, largeur_rectangle, hauteur_rectangle, couleur_fond, couleur_fond, 0.0), "")

                # Ajouter le texte par-dessus le rectangle "effaceur"
                igs.service_call("Whiteboard", "addText", (texte, 50.0, y_position, "#000000"), "")

                # Déplacer la position pour le prochain ordre affiché vers le bas
                y_position += 70.0  # Augmenter l'espacement entre les lignes pour éviter tout chevauchement

            print("[DEBUG] Historique du Whiteboard mis à jour.")
        except Exception as e:
            print(f"Erreur lors de la mise à jour du Whiteboard : {e}") """
    
    def process_remove_queue(self):
        while True:
            token = self.remove_queue.get()
            if token in self.elements_list:
                try:
                    igs.service_call("Whiteboard", "remove", (self.elements_list[token]), "")
                    self.elements_list.pop(token)
                    print(f"[DEBUG] Élément {token} supprimé du Whiteboard.")
                except Exception as e:
                    print(f"Erreur lors de la suppression de l'élément {token} : {e}")
            self.remove_queue.task_done()

    def mettre_a_jour_whiteboard(self):
        try:
            with self.lock:
                # Supprimer les anciens textes du Whiteboard
                for token in self.ordre_tokens:
                    if token in self.elements_list:
                        try:
                            igs.service_call("Whiteboard", "remove", (self.elements_list[token]), "")
                            self.elements_list.pop(token)  # Retirer également du dictionnaire local
                            print(f"[DEBUG] Élément {token} supprimé du Whiteboard.")
                        except Exception as e:
                            print(f"Erreur lors de la suppression de l'élément {token} : {e}")

                # Réinitialiser la liste des tokens
                self.ordre_tokens = []

                # Ajouter un titre pour l'historique
                if "titrehistorique" in self.elements_list:
                    try:
                        igs.service_call("Whiteboard", "remove", (self.elements_list["titrehistorique"]), "")
                        print(f"[DEBUG] Titre historique supprimé du Whiteboard.")
                    except Exception as e:
                        print(f"Erreur lors de la suppression du titre historique : {e}")

                titre = "Historique des derniers ordres :"
                igs.service_call("Whiteboard", "addText", (titre, 400.0, 490.0, "white"), "titrehistorique")

                # Réafficher les 5 derniers ordres
                derniers_ordres = self.ordre_historique[-5:]  # Ne garder que les 5 derniers
                y_position = 550.0  # Position initiale sur l'axe Y

                for i, ordre in enumerate(derniers_ordres):
                    trader_name, type_ordre, quantite, timestamp = ordre
                    texte = f"{timestamp} - {trader_name} - {type_ordre} : {quantite} jetons"

                    # Générer un token unique pour cet ordre
                    token = f"nouvelordre_{i + 1}"  # Ex : "nouvelordre_1", "nouvelordre_2", etc.
                    self.ordre_tokens.append(token)  # Ajouter ce token à la liste des ordres

                    # Ajouter le texte au Whiteboard avec un token unique
                    igs.service_call("Whiteboard", "addText", (texte, 220.0, y_position, "white"), token)

                    # Déplacer la position pour le prochain ordre
                    y_position += 70.0

                print("[DEBUG] Historique du Whiteboard mis à jour.")

        except Exception as e:
            print(f"Erreur lors de la mise à jour du Whiteboard : {e}")


    def update_price_continuously(self):
        # Mettre à jour le prix en sortie constamment
        while not self.stop_thread:
            self.prix_actuelO = self._prix
            time.sleep(0.5)  # Met à jour le prix toutes les 0.5 secondes

    def stop(self):
        # Arrêter la mise à jour continue du prix
        self.stop_thread = True
        self.update_thread.join()

    def elementCreated(self, sender_agent_name, sender_agent_uuid, Elementid, token):
        self.elements_list[token] = Elementid
        # add code here if needed