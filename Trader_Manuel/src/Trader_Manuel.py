#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

import ingescape as igs
import random
import uuid
import tkinter as tk
from tkinter import messagebox
import threading
import time
from datetime import datetime

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class TraderManuel:
    def __init__(self, nom=None):
        self.nom = nom  # Nom initial, qui sera défini par l'utilisateur lors de la création du compte
        self.uuid = str(uuid.uuid4())  # Générer un UUID unique pour chaque trader
        self.prix_actuel = 0.0  # Initialisation du prix actuel

        self.solde = 0.0  # Initialisation de la valeur du solde du compte récupéré de la banque
        self.jetons = 0  # Initialisation du nombre de jetons du compte récupéré de la banque

        # Créer un thread pour la fenêtre de création de compte
        self.account_creation_thread = threading.Thread(target=self.create_account_interface)
        self.account_creation_thread.daemon = True
        self.account_creation_thread.start()

    def create_account_interface(self):
        # Interface de création de compte
        self.account_window = tk.Tk()
        self.account_window.title("Création de Compte")

        # Champ pour saisir le nom
        tk.Label(self.account_window, text="Nom du Trader :", font=("Helvetica", 16)).grid(row=0, column=0, pady=10)
        self.entry_nom = tk.Entry(self.account_window, font=("Helvetica", 16))
        self.entry_nom.grid(row=0, column=1, pady=10)

        # Bouton pour créer le compte
        bouton_creer_compte = tk.Button(self.account_window, text="Créer Compte", command=self.creer_compte, font=("Helvetica", 16))
        bouton_creer_compte.grid(row=1, column=0, columnspan=2, pady=20)

        self.account_window.mainloop()

    def creer_compte(self):
        try:
            # Récupérer le nom
            nom = self.entry_nom.get()

            if nom:
                self.nom = nom
                # Envoyer la requête de création de compte à la banque
                igs.service_call("Banque", "creation_compte", (self.nom,), self.uuid)
                # Fermer la fenêtre de création de compte et ouvrir l'interface de trading
                self.account_window.destroy()
                self.account_window = None

                # Créer un thread pour l'interface de trading
                self.ui_thread = threading.Thread(target=self.create_interface)
                self.ui_thread.daemon = True
                self.ui_thread.start()

                # Créer un thread pour actualiser le solde automatiquement
                self.update_solde_thread = threading.Thread(target=self.actualiser_solde_en_continue)
                self.update_solde_thread.daemon = True
                self.update_solde_thread.start()

            else:
                messagebox.showerror("Erreur", "Veuillez entrer un nom valide.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la création du compte : {e}")

    # services
    def reponse_info_compte(self, sender_agent_name, sender_agent_uuid, solde, jetons):
        self.update_solde_label(solde, jetons)

    def create_interface(self):
        # Création de la fenêtre principale
        self.root = tk.Tk()
        self.root.title("Trader Manuel")

        # Création d'un cadre pour les boutons et les champs de saisie
        frame = tk.Frame(self.root)
        frame.pack(padx=20, pady=20)

        # Créer une étiquette pour le prix actuel
        self.label_prix_actuel = tk.Label(frame, text=f"Prix Actuel : {self.prix_actuel:.2f} euros", font=("Helvetica", 16))
        self.label_prix_actuel.grid(row=0, column=0, columnspan=2, pady=10)

        # Créer une étiquette et une entrée pour la quantité
        label_quantite = tk.Label(frame, text="Quantité :", font=("Helvetica", 16))
        label_quantite.grid(row=1, column=0, pady=10)

        self.entry_quantite = tk.Entry(frame, font=("Helvetica", 16), width=10)
        self.entry_quantite.grid(row=1, column=1, pady=10)

        # Configuration des boutons "Acheter" et "Vendre"
        bouton_acheter = tk.Button(frame, text="Acheter", command=self.acheter, bg="green", fg="black",
                                   font=("Helvetica", 24), width=10, height=2)
        bouton_vendre = tk.Button(frame, text="Vendre", command=self.vendre, bg="red", fg="black",
                                  font=("Helvetica", 24), width=10, height=2)

        # Placer les boutons sur la fenêtre
        bouton_acheter.grid(row=2, column=0, padx=10, pady=10)
        bouton_vendre.grid(row=2, column=1, padx=10, pady=10)

        # Créer un widget pour l'historique des ordres
        label_historique = tk.Label(self.root, text="Historique des ordres :", font=("Helvetica", 16))
        label_historique.pack(pady=10)

        self.text_historique = tk.Text(self.root, font=("Helvetica", 12), width=50, height=10)
        self.text_historique.pack(pady=10)

        # Ajouter une étiquette pour le solde
        self.label_solde = tk.Label(frame, text="Solde : 0 euros", font=("Helvetica", 16))
        self.label_solde.grid(row=3, column=0, columnspan=2, pady=10)

        # Ajouter une étiquette pour les jetons
        self.label_jetons = tk.Label(frame, text="Jetons : 0", font=("Helvetica", 16))
        self.label_jetons.grid(row=4, column=0, columnspan=2, pady=10)

        # Lancer l'interface graphique
        self.root.mainloop()

    def update_price_label(self):
        # Mise à jour de l'étiquette du prix dans l'interface graphique
        if hasattr(self, 'label_prix_actuel'):
            self.root.after(0, lambda: self.label_prix_actuel.config(text=f"Prix Actuel : {self.prix_actuel:.2f} euros"))

    def update_solde_label(self, solde, jetons):
        self.solde = solde
        self.jetons = jetons
        if hasattr(self, 'root'):
            self.root.after(0, lambda: self.label_solde.config(text=f"Solde : {self.solde:.2f} euros"))
            self.root.after(0, lambda: self.label_jetons.config(text=f"Jetons : {self.jetons}"))

    def actualiser_solde(self):
        try:
            # Appeler le service de la banque pour obtenir le solde et le nombre de jetons
            igs.service_call("Banque", "get_info_compte", (), self.uuid)
        except Exception as e:
            print(f"Erreur lors de l'envoi de la demande de solde : {e}")

    def actualiser_solde_en_continue(self):
        # Actualiser le solde toutes les 5 secondes
        while True:
            try:
                igs.service_call("Banque", "get_info_compte", (), self.uuid)
            except Exception as e:
                print(f"Erreur lors de l'envoi de la demande de solde : {e}")
            time.sleep(5)

    def ajouter_a_historique(self, texte):
        # Ajouter du texte à l'historique
        self.text_historique.insert(tk.END, texte + "\n")
        self.text_historique.see(tk.END)  # Scroll pour voir la dernière entrée

    def acheter(self):
        try:
            quantite = int(self.entry_quantite.get())
            montant_total = quantite * self.prix_actuel

            if quantite > 0:
                if montant_total > self.solde:
                    message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Achat refusé : {quantite} jetons (Solde insuffisant)"
                    messagebox.showwarning("Achat refusé", message)
                    self.ajouter_a_historique(message)
                else:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    igs.service_call("Banque", "ordre", (quantite, "acheter"), self.nom)
                    message = f"{timestamp} - acheter : {quantite} jetons"
                    messagebox.showinfo("Ordre d'achat", message)
                    self.ajouter_a_historique(message)
            else:
                messagebox.showwarning("Quantité invalide", "Veuillez entrer une quantité positive.")
        except ValueError:
            messagebox.showerror("Erreur de saisie", "Veuillez entrer une quantité valide.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'envoi de l'ordre d'achat : {e}")

    def vendre(self):
        try:
            quantite = int(self.entry_quantite.get())

            if quantite > 0:
                if quantite > self.jetons:
                    message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Vente refusée : {quantite} jetons (Jetons insuffisants)"
                    messagebox.showwarning("Vente refusée", message)
                    self.ajouter_a_historique(message)
                else:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    igs.service_call("Banque", "ordre", (quantite, "vendre"), self.nom)
                    message = f"{timestamp} - vendre : {quantite} jetons"
                    messagebox.showinfo("Ordre de vente", message)
                    self.ajouter_a_historique(message)
            else:
                messagebox.showwarning("Quantité invalide", "Veuillez entrer une quantité positive.")
        except ValueError:
            messagebox.showerror("Erreur de saisie", "Veuillez entrer une quantité valide.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'envoi de l'ordre de vente : {e}")