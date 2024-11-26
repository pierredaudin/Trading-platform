#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  Graphique.py
#  Graphique
#  Created by Ingenuity i/o on 2024/11/25
#
# "no description"
#
import ingescape as igs
import matplotlib
matplotlib.use('Agg')  # Utiliser un backend non interactif pour éviter les avertissements de GUI
import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
from datetime import datetime, timedelta
import os
import threading
import time
import base64

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Graphique:
    def __init__(self):
        self.prix_actuelI = 0.0
        self.prices_buffer = []  # To store price data for the current second
        self.data = []  # To store candlestick data
        self.lock = threading.Lock()

        # Start a thread to process and aggregate data every second
        self.aggregate_thread = threading.Thread(target=self.aggregate_data_per_second)
        self.aggregate_thread.daemon = True
        self.aggregate_thread.start()

        # Start a thread to update the Whiteboard image continuously
        self.whiteboard_update_thread = threading.Thread(target=self.update_whiteboard_continuously)
        self.whiteboard_update_thread.daemon = True
        self.whiteboard_update_thread.start()

        self.elements_list = {}

        # Créer une image de l'interface de trading
        self.creer_image_interface_trading()

        # Créer une image de l'interface de trading
        self.activer_maj_graphique=0

    def creer_image_interface_trading(self):
        try:
            # Créer une figure pour l'interface de trading (plus grande pour rendre l'interface plus visible)
            fig, ax = plt.subplots(figsize=(16, 12))

            # Fond de l'interface
            fig.patch.set_facecolor('#1c1c1e')  # Fond sombre

            # Zone du graphique (placeholder)
            graphique_rect = plt.Rectangle((0.05, 0.55), 0.8, 0.45, linewidth=2, edgecolor='white', facecolor='#2c2c2e')
            ax.add_patch(graphique_rect)
            plt.text(0.5, 0.75, 'Graphique (Trading)', color='white', fontsize=16, ha='center', va='center', transform=fig.transFigure)

            # Zone de l'historique des ordres
            historique_rect = plt.Rectangle((0.05, 0.05), 0.8, 0.45, linewidth=2, edgecolor='white', facecolor='#2c2c2e')
            ax.add_patch(historique_rect)
            #plt.text(0.5, 0.25, 'Historique des ordres', color='white', fontsize=16, ha='center', va='center', transform=fig.transFigure)

            # Simuler quelques éléments de l'interface
            ax.text(0.05, 0.95, 'UPSSI-Trading', color='white', fontsize=20, fontweight='bold', transform=fig.transFigure)
            ax.text(0.05, 0.90, 'Actif : UPS/EUR', color='white', fontsize=14, transform=fig.transFigure)
            #ax.text(0.75, 0.90, 'Solde : 1000 USDT', color='white', fontsize=14, transform=fig.transFigure)

            # Enlever les axes pour donner une apparence d'interface
            ax.axis('off')

            # Enregistrer l'image de l'interface de trading
            picture_dir = "Graphique/src/pictures"
            if not os.path.exists(picture_dir):
                os.makedirs(picture_dir)

            interface_image_path = os.path.join(picture_dir, 'interface_trading.png')
            plt.savefig(interface_image_path, bbox_inches='tight', facecolor=fig.get_facecolor())
            plt.close(fig)

            image_url = f"file:///{os.path.abspath(interface_image_path)}"

            # Mettre à jour le Whiteboard avec l'image de l'interface de trading
            igs.service_call("Whiteboard", "addImageFromUrl", (image_url, 0.0, -90.0), "interface")

            print("[DEBUG] Interface de trading créée avec succès.")
        except Exception as e:
            print(f"Erreur lors de la création de l'interface de trading : {e}")



    def aggregate_data_per_second(self):
        while True:
            time.sleep(1)  # Wait for one second

            # Lock access to the prices_buffer while aggregating data
            with self.lock:
                if len(self.prices_buffer) == 0:
                    continue

                # Create a candlestick for the past second
                open_price = self.prices_buffer[0]
                close_price = self.prices_buffer[-1]
                high_price = max(self.prices_buffer)
                low_price = min(self.prices_buffer)

                # Append the candlestick to the data list
                self.data.append({
                    'datetime': datetime.now(),
                    'open': open_price,
                    'high': high_price,
                    'low': low_price,
                    'close': close_price
                })

                # Clear the prices_buffer for the next second
                self.prices_buffer = []

            # Limit the data to the last 20 candles
            if len(self.data) > 30:
                self.data = self.data[-30:]

            # Update the graphical representation only if interface is displayed on whiteboard
            if self.activer_maj_graphique :
                self.mettre_a_jour_graphique()
            else :
                self.creer_image_interface_trading()

    def mettre_a_jour_graphique(self):
        try:
            # Use the last 20 data points to plot (or all, if fewer)
            df = pd.DataFrame(self.data)

            # Ensure we have enough data to generate a meaningful chart
            if len(df) < 2:
                return

            # Set the datetime as index for mplfinance compatibility
            df.set_index('datetime', inplace=True)

            # Plotting using mplfinance
            fig, ax = plt.subplots(figsize=(12, 5))  # Ajuster les dimensions pour mieux correspondre à l'espace sur l'interface
            mpf.plot(df, type='candle', ax=ax, style='charles')

            # Save the plot as an image with a unique name
            picture_dir = "Graphique/src/pictures"
            if not os.path.exists(picture_dir):
                os.makedirs(picture_dir)

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            picture_path = os.path.join(picture_dir, f'graphique_trading_{timestamp}.png')
            plt.savefig(picture_path, bbox_inches='tight')
            plt.close(fig)  # Close the figure to avoid memory leaks

            # Update the latest saved image path for the Whiteboard update thread
            self.latest_image_path = picture_path

            # Delete old images to avoid clutter
            self.supprimer_anciennes_images(picture_dir)

        except Exception as e:
            print(f"Erreur lors de la mise à jour du graphique : {e}")

    def supprimer_anciennes_images(self, picture_dir):
        try:
            # List all image files in the directory
            images = [f for f in os.listdir(picture_dir) if f.startswith('graphique_trading_') and f.endswith('.png')]
            # Sort files by creation time
            images.sort(key=lambda x: os.path.getctime(os.path.join(picture_dir, x)))

            # Keep only the last 5 images and delete the rest
            for image in images[:-5]:
                os.remove(os.path.join(picture_dir, image))
                # print(f"[DEBUG] Image supprimée : {image}")

        except Exception as e:
            print(f"Erreur lors de la suppression des anciennes images : {e}")

    def update_whiteboard_continuously(self):
        while True:
            try:
                # Update the whiteboard every 1 second with the latest image
                if hasattr(self, 'latest_image_path'):
                    self.update_whiteboard(self.latest_image_path)
                time.sleep(1)  # Adjust this sleep time as needed
            except Exception as e:
                print(f"Erreur lors de la mise à jour continue du Whiteboard : {e}")

    def update_whiteboard(self, image_path):
        try:
            if "graph" in self.elements_list:
                igs.service_call("Whiteboard", "remove", (self.elements_list["graph"]), "")
                # print(f"Element list {self.elements_list}")
            # Create the image URL for the Whiteboard
            image_url = f"file:///{os.path.abspath(image_path)}"

            # Update the Whiteboard with the image URL
            igs.service_call("Whiteboard", "addImageFromUrl", (image_url, 180.0, 10.0), "graph")
            # print(f"[DEBUG] Graphique mis à jour avec l'URL : {image_url}")


        except Exception as e:
            print(f"Erreur lors de la mise à jour du Whiteboard : {e}")

    def mettre_a_jour_prix_actuel(self, prix):
        try:
            # Add the new price to the buffer for the current second
            with self.lock:
                self.prices_buffer.append(prix)
        except Exception as e:
            print(f"Erreur lors de la mise à jour du prix actuel : {e}")


    # services
    def elementCreated(self, sender_agent_name, sender_agent_uuid, Elementid, token):
        self.elements_list[token] = Elementid
        if token == "interface":
            # Si c'est l'interface, lancer l'update du graphique après la confirmation de la création
            self.activer_maj_graphique = 1