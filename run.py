import json
import src.monitor_folder as monitor

# Charger la config
with open("config.json", "r") as f:
    config = json.load(f)

# Lancer la surveillance
monitor.monitor_folder(config["folder_to_monitor"])
