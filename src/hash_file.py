import hashlib

def hash_file(filepath, algo="sha256"):
    """Hache un fichier en utilisant l'algorithme spécifié."""
    hash_func = hashlib.new(algo)
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except FileNotFoundError:
        return "❌ Fichier introuvable."

# Exemple d'utilisation
if __name__ == "__main__":
    file_path = "../data/example.txt"
    print(f"SHA-256: {hash_file(file_path, 'sha256')}")
