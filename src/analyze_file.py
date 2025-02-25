import os
import sys
import time
import mimetypes
import hashlib
import stat
import magic
import uuid  # Récupération de l'ID unique de l'appareil
import socket  # Infos sur la machine locale
import platform  # OS, version, nom de l'ordinateur

# Importation correcte du module hash_file depuis src
try:
    from src.hash_file import hash_file
except ModuleNotFoundError:
    from hash_file import hash_file  # Alternative si exécuté depuis src/

# Importation des modules externes si disponibles
try:
    import exifread  # Métadonnées EXIF (images)
    import mutagen   # Métadonnées audio/vidéo
    from PyPDF2 import PdfReader  # Métadonnées PDF
except ImportError:
    exifread = None
    mutagen = None
    PdfReader = None

def get_file_hashes(filepath):
    """Calcule plusieurs hachages pour un fichier."""
    hash_algorithms = ["md5", "sha1", "sha256", "blake2b"]
    hashes = {}
    for algo in hash_algorithms:
        hashes[algo.upper()] = hash_file(filepath, algo)
    return hashes

def get_permissions(filepath):
    """Retourne les permissions du fichier sous forme lisible."""
    mode = os.stat(filepath).st_mode
    return {
        "Lecture": bool(mode & stat.S_IRUSR),
        "Écriture": bool(mode & stat.S_IWUSR),
        "Exécution": bool(mode & stat.S_IXUSR),
    }

def get_device_info():
    """Récupère des informations sur l'appareil qui exécute le script."""
    return {
        "Nom de l'ordinateur": socket.gethostname(),
        "Adresse IP locale": socket.gethostbyname(socket.gethostname()),
        "Système d'exploitation": platform.system(),
        "Version OS": platform.version(),
        "Architecture CPU": platform.architecture()[0],
        "ID unique de l'appareil": str(uuid.getnode()),  # Identifiant matériel
    }

def get_file_metadata(filepath):
    """Analyse détaillée des métadonnées du fichier."""
    if not os.path.exists(filepath):
        return {"Erreur": "❌ Fichier introuvable."}

    stat_info = os.stat(filepath)
    metadata = {
        "Nom": os.path.basename(filepath),
        "Taille": f"{stat_info.st_size} octets",
        "Créé le": time.ctime(stat_info.st_ctime),
        "Modifié le": time.ctime(stat_info.st_mtime),
        "Dernier accès": time.ctime(stat_info.st_atime),
        "Type MIME": magic.Magic(mime=True).from_file(filepath),
        "Hachages": get_file_hashes(filepath),
        "Permissions": get_permissions(filepath),
        "Infos Appareil": get_device_info(),
    }

    # Métadonnées spécifiques aux types de fichiers
    file_type = metadata["Type MIME"]
    
    if file_type.startswith("image") and exifread:
        metadata["EXIF"] = extract_exif_metadata(filepath)

    if file_type == "application/pdf" and PdfReader:
        metadata["PDF"] = extract_pdf_metadata(filepath)

    if file_type.startswith(("audio", "video")) and mutagen:
        metadata["Média"] = extract_media_metadata(filepath)

    return metadata

def extract_exif_metadata(filepath):
    """Récupère les métadonnées EXIF des images."""
    with open(filepath, "rb") as img_file:
        tags = exifread.process_file(img_file)
        exif_data = {tag: str(tags[tag]) for tag in tags if tag not in ["JPEGThumbnail", "TIFFThumbnail", "Filename", "EXIF MakerNote"]}

        # Ajout des données sur l'appareil photo ou smartphone utilisé
        if "Image Model" in exif_data:
            exif_data["Appareil Utilisé"] = exif_data["Image Model"]
        if "EXIF LensMake" in exif_data:
            exif_data["Fabricant"] = exif_data["EXIF LensMake"]
        if "EXIF LensModel" in exif_data:
            exif_data["Modèle Objectif"] = exif_data["EXIF LensModel"]

        return exif_data

def extract_pdf_metadata(filepath):
    """Récupère les métadonnées d'un PDF."""
    pdf = PdfReader(filepath)
    return pdf.metadata or {}

def extract_media_metadata(filepath):
    """Récupère les métadonnées des fichiers audio/vidéo."""
    media = mutagen.File(filepath, easy=True)
    return media.tags if media else {}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Utilisation : python analyze_file.py <chemin_du_fichier>")
        sys.exit(1)

    file_path = sys.argv[1]
    info = get_file_metadata(file_path)

    for key, value in info.items():
        print(f"{key} : {value}")
