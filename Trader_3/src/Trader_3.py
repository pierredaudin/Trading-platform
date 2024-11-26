#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  Trader_3.py
#  Trader_3
#  Created by Ingenuity i/o on 2024/11/26
#
# "no description"
#
import random
import ingescape as igs
import time
import uuid

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Trader3(metaclass=Singleton):
    def __init__(self, nom=None):
        self.nom = nom if nom else igs.agent_name()  # Utiliser le nom de l'agent comme nom du trader
        #self.jetons = 0  # Quantité initiale de jetons que le trader possède
        #self.argent = 1000  # Argent initial du trader
        self.uuid = str(uuid.uuid4())  # Générer un UUID unique pour chaque trader
        self.prix_actuel = 0.0

    def prendre_decision(self):
        print(f"{self.nom} prend une décision...")
        # Le trader décide aléatoirement d'acheter ou de vendre une certaine quantité de jetons
        type_ordre = random.choice(["acheter", "vendre"])
        quantite = random.randint(1, 10)
        return type_ordre, quantite

