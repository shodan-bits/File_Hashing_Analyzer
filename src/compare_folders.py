import os
import json
from utils import hash_file
from tqdm import tqdm

def compare_folders(folder1, folder2, algo="sha256"):
    """Compare deux dossiers et détecte les différences."""
    if not os.path.isdir(folder1) or not os.path.isdir(folder2):
        return "❌ Erreur : L'un des dossiers spécifiés n'existe pas."

    files1 = {f: hash_file(os.path.join(folder1, f), algo) for f in os.listdir(folder1) if os.path.isfile(os.path.join(folder1, f))}
    files2 = {f: hash_file(os.path.join(folder2, f), algo) for f in os.listdir(folder2) if os.path.isfile(os.path.join(folder2, f))}

    modified = []
    added = []
    deleted = []

    for file in files1:
        if file not in files2:
            deleted.append(file)
        elif files1[file] != files2[file]:
            modified.append(file)

    for file in files2:
        if file not in files1:
            added.append(file)

    report = {
        "Modifiés": modified,
        "Ajoutés": added,
        "Supprimés": deleted
    }

    print(json.dumps(report, indent=4, ensure_ascii=False))
    return report

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("❌ Utilisation : python src/compare_folders.py <dossier1> <dossier2> [--algo sha256]")
        sys.exit(1)

    folder1, folder2 = sys.argv[1], sys.argv[2]
    algo = "sha256"
    if "--algo" in sys.argv:
        algo = sys.argv[sys.argv.index("--algo") + 1]

    compare_folders(folder1, folder2, algo)
