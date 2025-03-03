import json

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport d'Analyse</title>
    <style>
        body { font-family: Arial, sans-serif; }
        table { width: 100%%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid black; padding: 10px; text-align: left; }
        th { background-color: #f4f4f4; }
    </style>
</head>
<body>
    <h1>Rapport d'Analyse</h1>
    <table>
        <tr><th>Fichier</th><th>Hachage</th></tr>
        {rows}
    </table>
</body>
</html>"""

def generate_html_report(json_file, output_html):
    """Génère un rapport HTML à partir d'un fichier JSON."""
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    rows = "".join(f"<tr><td>{file}</td><td>{hash}</td></tr>" for file, hash in data.items())

    with open(output_html, "w", encoding="utf-8") as f:
        f.write(HTML_TEMPLATE.format(rows=rows))

    print(f"📄 Rapport HTML généré : {output_html}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("❌ Utilisation : python src/generate_report.py <fichier.json> <sortie.html>")
        sys.exit(1)

    json_file, output_html = sys.argv[1], sys.argv[2]
    generate_html_report(json_file, output_html)
