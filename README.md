# 📂 FileAnalyzer

## 📌 Description
FileAnalyzer est un outil avancé permettant de hacher des fichiers, d'analyser leurs métadonnées, de surveiller les modifications dans un dossier et de vérifier l'intégrité des fichiers grâce à des signatures numériques. Il récupère également des informations détaillées sur l'appareil ayant créé le fichier.

⚠️ **Avertissement :** Ce projet est destiné à un usage éducatif et légal uniquement.

---

## 🚀 Installation

### 📥 1. Cloner le projet
Utilisez `git clone` pour récupérer le projet :
```bash
git clone https://github.com/shodan-bits/File_Hashing_Analyzer.git
cd File_Hashing_Analyzer
```

### 📦 2. Installer les dépendances
Dans le dossier du projet, exécutez :
```bash
pip install -r requirements.txt
```
Si `requirements.txt` est absent, installez manuellement :
```bash
pip install pycryptodome watchdog python-magic exifread mutagen pypdf2
```

---

## 🛠️ Utilisation

### 🔹 Hacher un fichier
```bash
python src/hash_file.py /chemin/vers/le/fichier
```

### 🔹 Analyser un fichier avec métadonnées avancées
```bash
python src/analyze_file.py /chemin/vers/le/fichier
```

🔍 **L'analyse inclut :**
- Hachages multiples (`MD5, SHA-1, SHA-256, BLAKE2b`)
- Informations sur l'appareil ayant créé le fichier (modèle, fabricant, objectif...)
- Permissions, dates de création/modification/accès
- Métadonnées EXIF (images), PDF, Audio/Vidéo
- Type MIME et structure du fichier

### 🔹 Surveiller un dossier
```bash
python src/monitor_folder.py /chemin/vers/le/dossier
```

### 🔹 Signer et vérifier un fichier
```bash
python src/sign_verify.py /chemin/vers/le/fichier
```

### 🔹 Exécuter tout le projet
```bash
python run.py
```

💡 **Remarque :** Le fichier ou dossier **n'a pas besoin d'être dans le même dossier que le programme**. Vous pouvez spécifier un **chemin absolu** (`/home/user/fichier.txt` ou `C:\Users\Nom\fichier.txt`) ou un **chemin relatif** (`../mon_fichier.txt`).

---

## 🛡️ Problèmes courants et solutions

### ❌ `PermissionError: [Errno 13] Permission denied`
- Assurez-vous que **le fichier ou le dossier n'est pas en cours d'utilisation**.
- Lancez le script en **mode administrateur**.

### ❌ `sqlite3.OperationalError: database is locked`
- Fermez les applications qui accèdent au fichier et réessayez.

### ❌ `ModuleNotFoundError: No module named 'Cryptodome'`
- Vérifiez si `pycryptodome` est bien installé avec :
  ```bash
  pip list | findstr Cryptodome
  ```
- Si absent, installez-le avec :
  ```bash
  pip install pycryptodome
  ```

---



