import re
import os
import sys
import yaml
import logging
from pathlib import Path

# === Configuration de la journalisation ===
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# === Constantes ===
YAML_FILE = "fl.md"

# === Table de correspondance (à éviter si possible) ===
ALIAS_MAP = {
    'a': 'yaml_key', 'b': 'regex_pattern', 'c': 'search_paths', 'd': 'root_dir',
    'e': 'search_files', 'f': 'patterns', 'g': 'pattern_paths', 'h': 'yaml_content',
    'x': 'parsed_yaml'
}

# === Définition des variables ===
DEFAULT_KEY = "clé_exemple"
DEFAULT_PATTERN = "motif_exemple"
DEFAULT_PATHS = ["chemin1", "chemin2"]
ROOT_DIR = ""
YAML_CONTENT = rf""" 
    base_path : 
    lauch_sh : ".sh"
    launch_py : 
    latex_file : 
    pdf_file : 
    path_vault:   example_vault  
    path_writing:   ✍Writing  
    path_templates:   👨‍💻Automations  
    path_table_block_template:   table_block.md  
    path_equation_block_template:   equation_block_single.md  
    path_equation_blocks:   equation blocks  
    path_table_blocks:   table blocks  
    path_list_note_paths:   DO_NOT_DELETE__note_paths.txt  
    path_BIBTEX:   BIBTEX  
"""

# === Fonctions ===
def load_yaml(yaml_string):
    """Charge le contenu YAML depuis une chaîne."""
    try:
        return yaml.safe_load(yaml_string)
    except yaml.YAMLError as e:
        logging.error(f"Erreur lors du chargement du YAML : {e}")
        return {}

def search_files(root_dir, regex_pattern, folders_first=True):
    """Recherche les fichiers et dossiers correspondant à un motif regex."""
    if not isinstance(regex_pattern, str) or not regex_pattern.strip():
        return []

    results = []
    try:
        for folder, subfolders, files in os.walk(Path(root_dir)):
            items = []
            if folders_first:
                items.extend(Path(folder) / d for d in subfolders)
                items.extend(Path(folder) / f for f in files)
            else:
                items.extend(Path(folder) / f for f in files)
                items.extend(Path(folder) / d for d in subfolders)

            for item in items:
                if re.search(regex_pattern, item.name, re.I):
                    results.append(str(item))
    except Exception as e:
        logging.error(f"Erreur lors de la recherche de motifs : {e}")
        return []

    return results

def load_patterns_from_yaml(filepath):
    """Charge les motifs depuis un fichier YAML."""
    try:
        with open(filepath, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        logging.warning(f"Fichier YAML non trouvé : {filepath}")
        return {}
    except yaml.YAMLError as e:
        logging.error(f"Erreur lors du chargement du YAML : {e}")
        return {}

def get_pattern_paths(patterns, root_dir):
    """Crée un dictionnaire avec les motifs et leurs chemins correspondants."""
    pattern_paths = {}
    for key, pattern in patterns.items():
        search_results = search_files(root_dir, pattern)
        if search_results:
            pattern_paths[key] = f"{pattern} --> {search_results[0]}"
        elif Path(pattern).exists():
            pattern_paths[key] = pattern
        else:
            pattern_paths[key] = "-- path non trouvé--"
    return pattern_paths

# === Script principal ===
if __name__ == "__main__":
    # 1. Charger les configurations et les variables
    logging.info("Début du script")
    parsed_yaml = load_yaml(YAML_CONTENT)
    root_dir = parsed_yaml.get("base_path", "") or Path(__file__).resolve().parent.parent

    # 2. Charger les motifs depuis le fichier YAML (fl.md)
    yaml_patterns = load_patterns_from_yaml(YAML_FILE)
    patterns = {
        key: str(yaml_patterns.get(key, "") or value or "")
        for key, value in parsed_yaml.items()
    }

    # 3. Créer le dictionnaire des chemins
    pattern_paths = get_pattern_paths(patterns, root_dir)

    # 4. Afficher les résultats
    for key, path in pattern_paths.items():
        logging.info(f"{key}: {path}")

    logging.info("Fin du script")

