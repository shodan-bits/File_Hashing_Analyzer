import sys
from utils import sign_file, save_signature, load_signature

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
        signature = sign_file(file_path, algo)
        print(f"🔑 Signature HMAC-{algo.upper()} : {signature}")
        if save:
            print(save_signature(file_path, signature, algo))

    elif action == "verify":
        expected_signature, used_algo = load_signature(file_path)
        if expected_signature is None:
            print("❌ Aucune signature trouvée pour ce fichier.")
        else:
            result = "✅ Fichier intact" if sign_file(file_path, used_algo) == expected_signature else "❌ Fichier modifié"
            print(result)

    else:
        print("❌ Action invalide. Utilisez 'sign' ou 'verify'.")

if __name__ == "__main__":
    main()
