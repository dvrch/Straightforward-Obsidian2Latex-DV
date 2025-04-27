import re
from pathlib import Path
import os
import yaml
import sys

# === EN-TÊTE : Table de correspondance ===
alias_map = {
    'a': 'cle', 'b': 'motif', 'c': 'chemins', 'd': 'racine', 'e': 'recherche_motifs',
    'f': 'motifs', 'g': 'cle_pattern_paths', 'h': 'fl', 'x': 'parsed_yaml',
}

# Fonction de synchronisation automatique des alias (robuste)
def sync_aliases():
    gbl = sys.modules[__name__].__dict__
    for alias, varname in alias_map.items():
        if varname in gbl:
            gbl[alias] = gbl[varname]

# --- DÉFINITION DES VARIABLES ---
cle = "clé_exemple"
motif = "motif_exemple"
chemins = ["chemin1", "chemin2"]
racine = ""
fl = rf"""
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
parsed_yaml = yaml.safe_load(fl)

# --- DÉFINITION DES FONCTIONS ET DICTIONNAIRES AVEC ALIAS ---
d = yaml.safe_load(fl)["base_path"] or Path(__file__).resolve().parent.parent

def recherche_motifs(d, b, dossier1st='d'):
    # On vérifie que b est bien une chaîne non vide
    if not isinstance(b, str) or not b.strip():
        return []
    return [
        str(item)
        for dossier, sous_dossiers, fichiers in os.walk(Path(d))
        for item in (
            [*(Path(dossier)/d for d in sous_dossiers), *(Path(dossier)/f for f in fichiers)]
            if dossier1st == 'd'
            else [*(Path(dossier)/f for f in fichiers), *(Path(dossier)/d for d in sous_dossiers)]
        )
        if re.search(b, item.name, re.I)
    ]

e = recherche_motifs  # alias

# Parsing YAML du string fl
md = Path("src/fl.md").resolve()
pars = {}
if md.exists():
    with open(md, encoding="utf-8") as f:
        try:
            pars = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"Erreur de YAML dans {md}: {e}")

p1 = parsed_yaml_var = yaml.safe_load(fl)

# Fusionner les dictionnaires p1 et pars
f = motifs = {**p1, **pars}

g = cle_pattern_paths = {
    a: ((f"{b} --> {c[0]}" if c else None)
    or (f"{Path(b)}" if Path(f"{b}").exists() else None)
    or "--path non trouvé--".strip()
    )
    for a, b in f.items()
    for c in [e(d, b)]
}

g1 = cle_pattern_paths = {
    a: ((f" = {c[0]}" if c else None)
    or (f"{Path(b)}" if Path(f"{b}").exists() else None)
    or f"= --path non trouvé--".strip("'")
    )
    for a, b in f.items()
    for c in [e(d, b)]
}

# Synchronisation initiale des alias (après définition des variables)
s = sync_aliases()
# print(a)  # Affiche: "nouvelle_clé"
