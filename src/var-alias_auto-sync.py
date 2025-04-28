# %%
import re
from pathlib import Path
import os
import yaml
import sys

import re
from typing import List

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

# %%
parsed_yaml = yaml.safe_load(fl)

# --- DÉFINITION DES FONCTIONS ET DICTIONNAIRES AVEC ALIAS ---
d =path = yaml.safe_load(fl)["base_path"] or Path(__file__).resolve().parent.parent

#  %%
def all_paths_in_folder(a__ = d):
    """Renvoie tous les chemins d'un répertoire donné."""
    A_paths =[os.path.join(root, file) 
              for root, dirs, files in os.walk(a__) 
              for file in files]
    return A_paths

# %%

# Parsing YAML du string fl


def find_matching_files(pattern: str, paths: List[str]) -> List[str]:
    """
    Trouve les fichiers correspondant au motif, en auto-détectant si c'est une regex ou un texte simple.
    - Si le motif contient des caractères regex spéciaux non échappés => traité comme regex
    - Sinon => traité comme texte simple (insensible à la casse)
    """
    # Détection automatique du type de motif
    if looks_like_regex(pattern):
        compiled_re = re.compile(pattern, re.IGNORECASE)
        return [p for p in paths if compiled_re.search(p)]
    else:
        pattern_lower = pattern.lower()
        return [p for p in paths if pattern_lower in p.lower()]

def looks_like_regex(pattern: str) -> bool:
    """Détecte si le motif semble être une regex (contient des caractères spéciaux non littéraux)."""
    regex_chars = {'\\', '.', '^', '$', '*', '+', '?', '{', '}', '[', ']', '|', '(', ')'}
    i = 0
    while i < len(pattern):
        if pattern[i] == '\\':
            i += 1  # Skip le prochain caractère (échappement)
        elif pattern[i] in regex_chars:
            return True
        i += 1
    return False
# %%
all_paths = all_paths_in_folder() or [
    'C:/dossier/fl.md',
    'C:/autre/dossier/FL.MD',
    'C:/test.txt',
    'C:/notes/literature.md'
]

# # Recherche textuelle automatique
# print(find_matching_files('fl.md', all_paths)) 
# # ['C:/dossier/fl.md', 'C:/autre/dossier/FL.MD']

# # Recherche regex automatique
# print(find_matching_files(r'fl\.md$', all_paths)) 
# # ['C:/dossier/fl.md', 'C:/autre/dossier/FL.MD', 'C:/notes/literature.md']

# # Mixte : texte avec caractère spécial échappé
# print(find_matching_files(r'literature\.md', all_paths))
# # ['C:/notes/literature.md']

# %%
zzz = find_matching_files(r'fl\.md$', all_paths)[0]
md = Path(zzz ).resolve()

def yaml_dict_content_from_file(md_file_path = md):

    """Lit un fichier Markdown, découpe par paragraphes et extrait les paires clé:valeur."""
    with open(md_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Découpage en paragraphes (séparés par 2 sauts de ligne ou plus)
    paragraphs = re.split(r'\n\s*\n', content.strip())
    
    result = {}
    for para in paragraphs:
        # Cherche une ligne "clé : valeur" au début du paragraphe
        match = re.match(r'^\s*([^:\n]+?)\s*:\s*(.+?)(?=\n\S|$)', para, re.DOTALL)
        if match:
            key, value = match.groups()
            key = key.strip()
            value = value.strip()
            
            # Essaye de parser la valeur comme YAML si elle contient des structures
            try:
                parsed_value = yaml.safe_load(value)
                if parsed_value is not None:  # Évite de convertir "None" en chaîne
                    value = parsed_value
            except:
                pass  # Garde la valeur originale si le parsing échoue
            
            result[key] = value
    
    return result

yaml_dict_content_from_file()


# %%
p1 = parsed_yaml_var = yaml.safe_load(fl)
# Fusionner les dictionnaires p1 et dict_from_file
f = motifs = {**p1, **dict_from_file}

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
m_a = ["vau", "path_writing", "path_templates"]
m_t = [(k, v) for k, v in g1.items() if m_a in k or m_a in v]
print(m_t)
