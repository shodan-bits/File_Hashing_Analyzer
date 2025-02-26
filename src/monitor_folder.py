import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from hash_file import hash_file  # Import du module de hachage

class MonitorHandler(FileSystemEventHandler):
    """Gère les modifications de fichiers dans un dossier."""
    def on_modified(self, event):
        if not event.is_directory:
            print(f"✏️ Fichier modifié : {event.src_path}")
            print(f"SHA-256: {hash_file(event.src_path)}")

def monitor_folder(folder):
    """Lance la surveillance d'un dossier."""
    if not os.path.exists(folder):
        print(f"❌ Le dossier '{folder}' n'existe pas.")
        return

    event_handler = MonitorHandler()
    observer = Observer()
    observer.schedule(event_handler, folder, recursive=True)
    observer.start()
    
    print(f"📡 Surveillance en cours du dossier : {folder}")
    
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
