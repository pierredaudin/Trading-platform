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

class Trader:
    def __init__(self, nom=None):
        self.nom = nom if nom else igs.agent_name()  # Utiliser le nom de l'agent comme nom du trader
        #self.jetons = 0  # Quantité initiale de jetons que le trader possède
        #self.argent = 1000  # Argent initial du trader
        self.uuid = str(uuid.uuid4())  # Générer un UUID unique pour chaque trader
        self.prix_actuel = 0.0


    """  def get_prix_actuel(self):
        self.prix_actuel = igs.input_get_double("prix_actuel")
        if self._prix is not None:
            igs.output_set_double("prix_actuel", self._prix)  # Utiliser un double pour représenter les valeurs flottantes
            print(f"Prix actuel mis à jour : {self._prix:.2f} euros") """

    def prendre_decision(self):
        print(f"{self.nom} prend une décision...")
        # Le trader décide aléatoirement d'acheter ou de vendre une certaine quantité de jetons
        type_ordre = random.choice(["acheter", "vendre"])
        quantite = random.randint(1, 10)
        return type_ordre, quantite


    """ def effectuer_ordre(self):
        time.sleep(2)  # Pause de 2 secondes avant de placer un ordre
        self.prix_actuel = igs.input_get_double("prix_actuel") #récupération du prix actuel
        print(f"{self.nom} effectue un ordre...")
        # Prendre une décision et l'envoyer à la banque
        type_ordre, quantite = self.prendre_decision()
        if type_ordre == "acheter" and self.argent >= quantite * self.prix_actuel:
            print(f"{self.nom} tente d'acheter {quantite} jetons à {self.prix_actuel} euros chacun.")
            arguments_ordre = (quantite,type_ordre)
            igs.service_call("Banque", "ordre", arguments_ordre, str(self.nom))
            self.argent -= quantite * self.prix_actuel
            self.jetons += quantite
        elif type_ordre == "vendre" and self.jetons >= quantite:
            print(f"{self.nom} tente de vendre {quantite} jetons à {self.prix_actuel} euros chacun.")
            arguments_ordre = (quantite,type_ordre)
            igs.service_call("Banque", "ordre", arguments_ordre, str(self.nom))
            self.argent += quantite * self.prix_actuel
            self.jetons -= quantite
        else:
            print(f"{self.nom} n'a pas pu effectuer l'ordre : {type_ordre} de {quantite} jetons. Il possède {self.jetons} jetons et {self.argent} euros.")
            print(f"{self.nom} ne peut pas effectuer l'ordre : {type_ordre} {quantite} jetons.")
 """