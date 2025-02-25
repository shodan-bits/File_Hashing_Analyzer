import os
import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from hash_file import hash_file

class MonitorHandler(FileSystemEventHandler):
    """Gère les modifications de fichiers dans un dossier."""
    def on_modified(self, event):
        if not event.is_directory:
            print(f"✏️ Fichier modifié : {event.src_path}")
            print(f"SHA-256: {hash_file(event.src_path)}")

def monitor_folder(folder):
    """Lance la surveillance d'un dossier."""
    event_handler = MonitorHandler()
    observer = Observer()
    observer.schedule(event_handler, folder, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Exemple d'utilisation
if __name__ == "__main__":
    folder_to_monitor = "../data/"
    print(f"📡 Surveillance du dossier : {folder_to_monitor}")
    monitor_folder(folder_to_monitor)
