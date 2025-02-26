import os
import json
import hashlib
import hmac

SECRET_KEY = b"SuperSecretKey"
SIGNATURES_FILE = "logs/signatures.json"
os.makedirs("logs", exist_ok=True)  # Crée le dossier logs s'il n'existe pas

def hash_file(filepath, algo="sha256", buffer_size=65536):
    """Hache un fichier avec l'algorithme spécifié en lecture streaming."""
    if not os.path.exists(filepath):
        return "❌ Fichier introuvable."

    if algo.lower() not in hashlib.algorithms_available:
        return f"❌ Algorithme non supporté. Choisissez parmi : {', '.join(hashlib.algorithms_available)}"

    hash_func = hashlib.new(algo.lower())

    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(buffer_size), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except Exception as e:
        return f"❌ Erreur lors du hachage : {str(e)}"

def sign_file(filepath, algo="sha256"):
    """Génère une signature HMAC pour un fichier."""
    file_hash = hash_file(filepath, algo)
    if "❌" in file_hash:
        return file_hash  # Erreur retournée

    return hmac.new(SECRET_KEY, file_hash.encode(), hashlib.sha256).hexdigest()

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

        return f"📂 Signature enregistrée dans {SIGNATURES_FILE}"
    except Exception as e:
        return f"❌ Erreur lors de l'enregistrement : {str(e)}"

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
        return f"❌ Erreur de lecture des signatures : {str(e)}", None
