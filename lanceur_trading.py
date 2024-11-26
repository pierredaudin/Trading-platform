import subprocess
import os
import time
from PyQt5.QtWidgets import QApplication, QFileDialog

# Définitions des chemins par défaut basés sur le répertoire actuel
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
WHITEBOARD_PATH = os.path.join(BASE_DIR, "Whiteboard_EXE", "Whiteboard.exe")
IGSSYSTEM_PATH = os.path.join(BASE_DIR, "UPSSI_Trading.igssystem")

# Les chemins des scripts Python
scripts = {
    "Banque": os.path.join(BASE_DIR, "Banque/src/main.py"),
    "Graphique": os.path.join(BASE_DIR, "Graphique/src/main.py"),
    "Trader_Manuel": os.path.join(BASE_DIR, "Trader_Manuel/src/main.py"),
    "Trader_1": os.path.join(BASE_DIR, "Trader_1/src/main.py"),
    "Trader_2": os.path.join(BASE_DIR, "Trader_2/src/main.py"),
    "Trader_3": os.path.join(BASE_DIR, "Trader_3/src/main.py"),
    "Trader_4": os.path.join(BASE_DIR, "Trader_4/src/main.py"),
    "Trader_5": os.path.join(BASE_DIR, "Trader_5/src/main.py"),
    "Trader": os.path.join(BASE_DIR, "Trader/src/main.py")
}


def start_app():
    """
    Ouvrir une fenêtre avec Qt pour choisir l'exécutable d'Ingescape Circle.
    Par défaut, va dans le répertoire où Ingescape Circle v4 devrait être.
    """
    app = QApplication([])  # Initialisation de l'application PyQt

    # Répertoire par défaut
    default_directory = r"C:\Program Files\Ingescape\Ingescape Circle v4"
    if not os.path.exists(default_directory):
        print(f"Default directory '{default_directory}' does not exist. Using current directory instead.")
        default_directory = ""  # Utilise le répertoire courant si le chemin par défaut n'existe pas

    file_path, _ = QFileDialog.getOpenFileName(
        None,
        "Select the Ingescape Circle v4 executable",  # Titre de la boîte de dialogue
        default_directory,  # Répertoire de départ
        "Executable Files (*.exe)"  # Filtre pour fichiers exécutables
    )
    return file_path if file_path else None


def start_process(ingescape_path, port="5670", device="Wi-Fi"):
    """
    Start all required processes and monitor them.
    """
    processes = []

    try:
        # Launch processes and add them to the list
        if os.path.exists(WHITEBOARD_PATH):
            processes.append(subprocess.Popen([WHITEBOARD_PATH, '--port', port, '--device', device]))
            print("Whiteboard launched.")
        else:
            print(f"Whiteboard executable not found: {WHITEBOARD_PATH}")

        if os.path.exists(IGSSYSTEM_PATH):
            processes.append(subprocess.Popen([ingescape_path, IGSSYSTEM_PATH, '--port', port, '--device', device]))
            print("Ingescape Circle launched.")
        else:
            print(f"Ingescape system file not found: {IGSSYSTEM_PATH}")

        # Démarrer les scripts Python
        for script_name, script_path in scripts.items():
            if os.path.exists(script_path):
                processes.append(subprocess.Popen(["python", script_path, '--port', port, '--device', device]))
                print(f"{script_name} launched.")
            else:
                print(f"{script_name} script not found: {script_path}")

    except Exception as e:
        print(f"Failed to launch a process: {e}")
        kill_process(processes)
        return

    # Monitor processes in a loop
    try:
        while True:
            time.sleep(1)  # Check every second
            for process in processes:
                if process.poll() is not None:  # Process terminated
                    print("One process has terminated. Stopping all processes.")
                    kill_process(processes)
                    return
    except KeyboardInterrupt:
        print("Interrupt signal received. Stopping all processes.")
        kill_process(processes)


def kill_process(processes):
    """
    Terminate all running processes.
    """
    for process in processes:
        try:
            if process.poll() is None:  # Check if the process is still running
                process.terminate()
                print(f"Terminated process {process.pid}.")
        except Exception as e:
            print(f"Error terminating process: {e}")


if __name__ == "__main__":
    # Sélectionner l'exécutable via une boîte de dialogue
    ingescape_circle_path = start_app()

    if not ingescape_circle_path:
        print("Pas d'executable sélectionné")
    else:
        print(f"Executable sélectionné: {ingescape_circle_path}")
        # Lancer les processus avec les paramètres par défaut
        start_process(ingescape_circle_path)
