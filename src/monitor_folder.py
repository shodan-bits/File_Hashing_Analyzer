import os
import sys
import time
import json
import hashlib
import stat
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
from hash_file import hash_file  # Import du module de hachage

# Configuration du logging
LOG_FILE = "logs/monitoring.log"
JSON_LOG_FILE = "logs/log.json"

os.makedirs("logs", exist_ok=True)  # Créer le dossier logs s'il n'existe pas

logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

class AdvancedMonitorHandler(FileSystemEventHandler):
    """Gère tous les événements sur les fichiers et dossiers surveillés."""

    def on_modified(self, event):
        """Détecte une modification de fichier."""
        if not event.is_directory:
            info = get_file_info(event.src_path)
            print(f"✏️ Fichier modifié : {event.src_path}")
            print(json.dumps(info, indent=4))
            log_event("modification", event.src_path, info)

    def on_created(self, event):
        """Détecte la création d'un fichier ou dossier."""
        info = get_file_info(event.src_path)
        print(f"🆕 Nouveau fichier/dossier : {event.src_path}")
        print(json.dumps(info, indent=4))
        log_event("création", event.src_path, info)

    def on_deleted(self, event):
        """Détecte la suppression d'un fichier ou dossier."""
        print(f"🗑️ Fichier/Dossier supprimé : {event.src_path}")
        log_event("suppression", event.src_path, None)

    def on_moved(self, event):
        """Détecte le renommage ou déplacement d'un fichier."""
        print(f"🔄 Fichier renommé/déplacé : {event.src_path} → {event.dest_path}")
        log_event("déplacement", event.dest_path, {"ancien_chemin": event.src_path})

def get_file_info(filepath):
    """Récupère les métadonnées détaillées d'un fichier."""
    if not os.path.exists(filepath):
        return {"Erreur": "Fichier introuvable"}

    stat_info = os.stat(filepath)
    return {
        "Nom": os.path.basename(filepath),
        "Taille": f"{stat_info.st_size} octets",
        "Créé le": datetime.fromtimestamp(stat_info.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
        "Modifié le": datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
        "Dernier accès": datetime.fromtimestamp(stat_info.st_atime).strftime('%Y-%m-%d %H:%M:%S'),
        "SHA-256": hash_file(filepath, "sha256"),
        "Permissions": {
            "Lecture": bool(stat_info.st_mode & stat.S_IRUSR),
            "Écriture": bool(stat_info.st_mode & stat.S_IWUSR),
            "Exécution": bool(stat_info.st_mode & stat.S_IXUSR),
        }
    }

def log_event(event_type, path, details):
    """Enregistre l'événement dans un fichier JSON et dans les logs."""
    log_entry = {
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "type": event_type,
        "chemin": path,
        "détails": details
    }

    logging.info(json.dumps(log_entry, ensure_ascii=False))

    # Ajouter l'événement au fichier JSON
    if os.path.exists(JSON_LOG_FILE):
        with open(JSON_LOG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    data.append(log_entry)

    with open(JSON_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def monitor_folder(folder):
    """Lance la surveillance avancée d'un dossier et de ses sous-dossiers."""
    if not os.path.exists(folder):
        print(f"❌ Le dossier '{folder}' n'existe pas.")
        return

    event_handler = AdvancedMonitorHandler()
    observer = Observer()
    observer.schedule(event_handler, folder, recursive=True)  # 🔥 Surveillance récursive activée
    observer.start()

    print(f"📡 Surveillance avancée activée pour : {folder}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n📴 Surveillance arrêtée.")
    observer.join()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Utilisation : python src/monitor_folder.py <chemin_du_dossier>")
        sys.exit(1)

    folder_to_monitor = sys.argv[1]
    monitor_folder(folder_to_monitor)
