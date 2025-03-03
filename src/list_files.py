import os
import json
from tqdm import tqdm
from utils import hash_file

def list_files(directory, algo="sha256", output_file=None):
    """Liste tous les fichiers d'un dossier et calcule leurs hachages."""
    if not os.path.isdir(directory):
        return f"❌ Erreur : Le dossier '{directory}' n'existe pas."

    files_data = {}
    files = sorted([os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])

    print(f"📂 Liste des fichiers dans {directory}...\n")

    for file in tqdm(files, desc="🔍 Calcul des hachages", unit=" fichier"):
        files_data[file] = hash_file(file, algo)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(files_data, f, indent=4, ensure_ascii=False)
        print(f"📄 Rapport sauvegardé dans {output_file}")

    return files_data

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("❌ Utilisation : python src/list_files.py <chemin_du_dossier> [--algo sha256] [--output result.json]")
        sys.exit(1)

    directory = sys.argv[1]
    algo = "sha256"
    output_file = None

    if "--algo" in sys.argv:
        algo = sys.argv[sys.argv.index("--algo") + 1]
    if "--output" in sys.argv:
        output_file = sys.argv[sys.argv.index("--output") + 1]

    list_files(directory, algo, output_file)
