import hmac
import hashlib

SECRET_KEY = b"SuperSecretKey"

def sign_file(filepath):
    """Génère une signature HMAC pour le fichier."""
    try:
        with open(filepath, "rb") as f:
            file_data = f.read()
        return hmac.new(SECRET_KEY, file_data, hashlib.sha256).hexdigest()
    except FileNotFoundError:
        return "❌ Fichier introuvable."

def verify_file(filepath, expected_signature):
    """Vérifie si la signature du fichier est valide."""
    return sign_file(filepath) == expected_signature

# Exemple d'utilisation
if __name__ == "__main__":
    file_path = "../data/example.txt"
    signature = sign_file(file_path)
    print(f"Signature : {signature}")
    print(f"Vérification : {'✅ OK' if verify_file(file_path, signature) else '❌ Modifié'}")
