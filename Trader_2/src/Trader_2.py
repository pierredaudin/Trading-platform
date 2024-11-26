#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  Trader.py
#  Trader
#  Created by Ingenuity i/o on 2024/11/22
#
# "no description"
#
import random
import ingescape as igs
import time
import uuid

class Trader2:
    def __init__(self, nom=None):
        self.nom = nom if nom else igs.agent_name()  # Utiliser le nom de l'agent comme nom du trader
        self.jetons = 0  # Quantité initiale de jetons que le trader possède
        self.argent = 1000  # Argent initial du trader
        self.uuid = str(uuid.uuid4())  # Générer un UUID unique pour chaque trader

    def prendre_decision(self):
        print(f"{self.nom} prend une décision...")
        # Le trader décide aléatoirement d'acheter ou de vendre une certaine quantité de jetons
        type_ordre = random.choice(["acheter", "vendre"])
        quantite = random.randint(1, 10)
        return type_ordre, quantite


    """  def effectuer_ordre(self, banque):
        time.sleep(2)  # Pause de 2 secondes avant de placer un ordre
        print(f"{self.nom} effectue un ordre...")
        # Prendre une décision et l'envoyer à la banque
        type_ordre, quantite = self.prendre_decision()
        if type_ordre == "acheter" and self.argent >= quantite * banque.prix_actuelO:
            print(f"{self.nom} tente d'acheter {quantite} jetons à {banque.prix_actuelO} euros chacun.")
            banque.ordre(self.nom, None, type_ordre, quantite)
            self.argent -= quantite * banque.prix_actuelO
            self.jetons += quantite
        elif type_ordre == "vendre" and self.jetons >= quantite:
            print(f"{self.nom} tente de vendre {quantite} jetons à {banque.prix_actuelO} euros chacun.")
            banque.ordre(self.nom, None, type_ordre, quantite)
            self.argent += quantite * banque.prix_actuelO
            self.jetons -= quantite
        else:
            print(f"{self.nom} n'a pas pu effectuer l'ordre : {type_ordre} de {quantite} jetons. Il possède {self.jetons} jetons et {self.argent} euros.")
            print(f"{self.nom} ne peut pas effectuer l'ordre : {type_ordre} {quantite} jetons.")
    """