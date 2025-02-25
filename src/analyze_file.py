import os
import sys
import time
from hash_file import hash_file  # Assurez-vous que hash_file.py est bien dans le même dossier

def analyze_file(filepath):
    """Analyse un fichier : taille, date de modification, hachage."""
    if not os.path.exists(filepath):
        return "❌ Fichier introuvable."

    stat = os.stat(filepath)
    return {
        "Nom": os.path.basename(filepath),
        "Taille": f"{stat.st_size} octets",
        "Modifié le": time.ctime(stat.st_mtime),
        "SHA-256": hash_file(filepath, "sha256"),  # Utilisation de SHA-256
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Utilisation : python analyze_file.py <chemin_du_fichier>")
        sys.exit(1)

    file_path = sys.argv[1]

    # Vérification et affichage des résultats
    info = analyze_file(file_path)
    if isinstance(info, dict):
        for k, v in info.items():
            print(f"{k} : {v}")
    else:
        print(info)  # Affiche l'erreur si le fichier est introuvable
