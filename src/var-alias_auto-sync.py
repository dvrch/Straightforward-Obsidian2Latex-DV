# %%
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

# %%
parsed_yaml = yaml.safe_load(fl)

# --- DÉFINITION DES FONCTIONS ET DICTIONNAIRES AVEC ALIAS ---
d =path = yaml.safe_load(fl)["base_path"] or Path(__file__).resolve().parent.parent

#  %%
def all_paths_in_folder(a__ = d):
    """Renvoie tous les chemins d'un répertoire donné."""
    A_paths =[os.path.join(root, file) 
              for root, dirs, files in os.walk(path) 
              for file in files]
    return A_paths

# %%

# Parsing YAML du string fl
# md = Path("fl.md").resolve()
md = re.match(r"fl.md", all_paths_in_folder()) ; md = 
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
