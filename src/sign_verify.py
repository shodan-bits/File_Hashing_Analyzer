import hmac
import hashlib
import sys
import os
import json
from tqdm import tqdm

SECRET_KEY = b"SuperSecretKey"
SIGNATURES_FILE = "logs/signatures.json"
os.makedirs("logs", exist_ok=True)  # Création du dossier logs si absent

SUPPORTED_ALGORITHMS = ["sha256", "sha512", "blake2b", "sha3_256"]

def sign_file(filepath, algo="sha256", save=False):
    """Génère une signature HMAC pour un fichier."""
    if not os.path.exists(filepath):
        return "❌ Fichier introuvable."

    if algo.lower() not in SUPPORTED_ALGORITHMS:
        return f"❌ Algorithme non supporté. Choisissez parmi : {', '.join(SUPPORTED_ALGORITHMS)}"

    hash_func = hashlib.new(algo.lower())

    try:
        with open(filepath, "rb") as f:
            for chunk in tqdm(iter(lambda: f.read(65536), b""), desc="🔑 Hachage en cours", unit=" bloc"):
                hash_func.update(chunk)

        signature = hmac.new(SECRET_KEY, hash_func.digest(), hashlib.sha256).hexdigest()

        if save:
            save_signature(filepath, signature, algo)

        return signature
    except Exception as e:
        return f"❌ Erreur : {str(e)}"

def save_signature(filepath, signature, algo):
    """Enregistre la signature d’un fichier dans un fichier JSON."""
    try:
        if os.path.exists(SIGNATURES_FILE):
            with open(SIGNATURES_FILE, "r", encoding="utf-8") as f:
                signatures = json.load(f)
        else:
            signatures = {}

        signatures[filepath] = {"signature": signature, "algo": algo}

        with open(SIGNATURES_FILE, "w", encoding="utf-8") as f:
            json.dump(signatures, f, indent=4, ensure_ascii=False)

        print(f"📂 Signature enregistrée dans {SIGNATURES_FILE}")
    except Exception as e:
        print(f"❌ Erreur lors de l'enregistrement : {str(e)}")

def verify_file(filepath, expected_signature, algo="sha256"):
    """Vérifie si la signature d’un fichier est valide."""
    actual_signature = sign_file(filepath, algo)

    if actual_signature == "❌ Fichier introuvable.":
        return actual_signature

    if actual_signature == expected_signature:
        return "✅ Fichier intact"
    else:
        return f"❌ Fichier modifié !\n🔍 Signature attendue : {expected_signature}\n🔍 Signature actuelle : {actual_signature}"

def load_signature(filepath):
    """Charge une signature depuis le fichier JSON."""
    try:
        if not os.path.exists(SIGNATURES_FILE):
            return None, None

        with open(SIGNATURES_FILE, "r", encoding="utf-8") as f:
            signatures = json.load(f)

        if filepath in signatures:
            return signatures[filepath]["signature"], signatures[filepath]["algo"]

        return None, None
    except Exception as e:
        print(f"❌ Erreur de lecture des signatures : {str(e)}")
        return None, None

def main():
    """Gestion des arguments en ligne de commande."""
    if len(sys.argv) < 3:
        print("❌ Utilisation :")
        print("   - Générer une signature : python src/sign_verify.py sign <chemin_du_fichier> [--algo sha256] [--save]")
        print("   - Vérifier une signature : python src/sign_verify.py verify <chemin_du_fichier>")
        sys.exit(1)

    action = sys.argv[1]
    file_path = sys.argv[2]
    algo = "sha256"
    save = "--save" in sys.argv
    if "--algo" in sys.argv:
        algo_index = sys.argv.index("--algo") + 1
        if algo_index < len(sys.argv):
            algo = sys.argv[algo_index]

    if action == "sign":
        signature = sign_file(file_path, algo, save)
        print(f"🔑 Signature HMAC-{algo.upper()} : {signature}")

    elif action == "verify":
        expected_signature, used_algo = load_signature(file_path)
        if expected_signature is None:
            print("❌ Aucune signature trouvée pour ce fichier.")
        else:
            result = verify_file(file_path, expected_signature, used_algo)
            print(result)

    else:
        print("❌ Action invalide. Utilisez 'sign' ou 'verify'.")

if __name__ == "__main__":
    main()
