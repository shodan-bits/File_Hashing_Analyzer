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
pip install pycryptodome watchdog python-magic exifread mutagen pypdf2 tqdm
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

### 🔹 Signer un fichier et vérifier son intégrité
#### ✏️ **Générer une signature HMAC**
```bash
python src/sign_verify.py sign /chemin/vers/le/fichier --algo sha512 --save
```
📌 Cela génère une signature HMAC avec l'algorithme SHA-512 et l'enregistre dans `logs/signatures.json`.

#### 🔍 **Vérifier un fichier avec sa signature enregistrée**
```bash
python src/sign_verify.py verify /chemin/vers/le/fichier
```
📌 Cela compare le fichier avec sa signature et indique s'il a été **modifié ou non**.

### 🔹 Lister tous les fichiers d’un dossier avec leurs hachages
```bash
python src/list_files.py "C:\Users\shodan\Documents\" --algo sha512 --output result.json

```
### 🔹 Générer un rapport HTML des fichiers analysés
``` bash
python src/generate_report.py result.json report.html


```
### 🔹  Comparer deux dossiers pour détecter les changements
```bash
python src/compare_folders.py "C:\Backup1" "C:\Backup2" --algo sha256

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

