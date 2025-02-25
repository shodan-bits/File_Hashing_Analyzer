import os
import time
from hash_file import hash_file

def analyze_file(filepath):
    """Analyse un fichier : taille, date de modification, hachage."""
    if not os.path.exists(filepath):
        return "❌ Fichier introuvable."

    stat = os.stat(filepath)
    return {
        "Nom": os.path.basename(filepath),
        "Taille": f"{stat.st_size} octets",
        "Modifié le": time.ctime(stat.st_mtime),
        "SHA-256": hash_file(filepath, "sha256"),
    }

# Exemple d'utilisation
if __name__ == "__main__":
    file_path = "../data/example.txt"
    info = analyze_file(file_path)
    for k, v in info.items():
        print(f"{k} : {v}")
