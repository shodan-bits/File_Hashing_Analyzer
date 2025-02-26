import os
import sys
import json
import hashlib
import argparse
from tqdm import tqdm  # Pour afficher la barre de progression

# Liste des algorithmes de hachage supportés
SUPPORTED_ALGORITHMS = hashlib.algorithms_available

def hash_file(filepath, algo="sha256", buffer_size=65536):
    """Hache un fichier en utilisant un algorithme donné et une lecture par buffer."""
    if not os.path.exists(filepath):
        return f"❌ Erreur : Le fichier '{filepath}' n'existe pas."

    if algo.lower() not in SUPPORTED_ALGORITHMS:
        return f"❌ Erreur : Algorithme '{algo}' non supporté. Choisissez parmi : {', '.join(SUPPORTED_ALGORITHMS)}"

    hash_func = hashlib.new(algo.lower())

    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(buffer_size), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except Exception as e:
        return f"❌ Erreur lors du hachage : {str(e)}"

def hash_directory(directory, algo="sha256", output_file=None):
    """Hache tous les fichiers d'un dossier et génère un rapport JSON."""
    if not os.path.isdir(directory):
        return f"❌ Erreur : Le dossier '{directory}' n'existe pas."

    results = {}
    files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    print(f"🔍 Hachage de {len(files)} fichiers dans {directory}...\n")

    for file in tqdm(files, desc="Hachage en cours", unit=" fichier"):
        results[file] = hash_file(file, algo)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
        print(f"📂 Résultats sauvegardés dans {output_file}")

    return results

def compare_files(file1, file2, algo="sha256"):
    """Compare les hachages de deux fichiers pour vérifier s'ils sont identiques."""
    hash1 = hash_file(file1, algo)
    hash2 = hash_file(file2, algo)

    if hash1 == hash2:
        return f"✅ Les fichiers {file1} et {file2} sont identiques ({algo.upper()})"
    else:
        return f"❌ Les fichiers {file1} et {file2} sont différents ({algo.upper()})"

def main():
    """Gère les arguments en ligne de commande."""
    parser = argparse.ArgumentParser(description="Outil avancé de hachage de fichiers et de dossiers.")
    
    parser.add_argument("path", help="Chemin du fichier ou du dossier à hacher")
    parser.add_argument("-a", "--algo", default="sha256", help=f"Algorithme de hachage (par défaut : SHA-256). Options : {', '.join(SUPPORTED_ALGORITHMS)}")
    parser.add_argument("-o", "--output", help="Fichier de sortie JSON pour enregistrer les hachages")
    parser.add_argument("-c", "--compare", nargs=2, help="Comparer deux fichiers (exemple : -c fichier1 fichier2)")

    args = parser.parse_args()

    if args.compare:
        result = compare_files(args.compare[0], args.compare[1], args.algo)
        print(result)
    elif os.path.isdir(args.path):
        hash_directory(args.path, args.algo, args.output)
    elif os.path.isfile(args.path):
        hash_value = hash_file(args.path, args.algo)
        print(f"🔑 Hachage {args.algo.upper()} de {args.path} : {hash_value}")
    else:
        print("❌ Erreur : Chemin invalide. Veuillez fournir un fichier ou un dossier valide.")

if __name__ == "__main__":
    main()
