# 📂 FileAnalyzer

## 📌 Description
FileAnalyzer est un outil permettant de hacher des fichiers, d'analyser leurs métadonnées, de surveiller les modifications dans un dossier et de vérifier l'intégrité des fichiers grâce à des signatures numériques.

⚠️ **Avertissement :** Ce projet est destiné à un usage éducatif et légal uniquement.

---

## 🚀 Installation

### 📥 1. Installer Python
Assurez-vous d'avoir **Python 3.10+** installé. Téléchargez-le depuis [python.org](https://www.python.org/downloads/).

### 📦 2. Installer les dépendances
Dans le dossier du projet, exécutez :
```bash
pip install -r requirements.txt
```
Si `requirements.txt` est absent, installez manuellement :
```bash
pip install pycryptodome watchdog
```

---

## 🛠️ Utilisation

### 🔹 Hacher un fichier
```bash
python src/hash_file.py chemin_du_fichier
```

### 🔹 Analyser un fichier
```bash
python src/analyze_file.py chemin_du_fichier
```

### 🔹 Surveiller un dossier
```bash
python src/monitor_folder.py chemin_du_dossier
```

### 🔹 Signer et vérifier un fichier
```bash
python src/sign_verify.py chemin_du_fichier
```

### 🔹 Exécuter tout le projet
```bash
python run.py
```

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


