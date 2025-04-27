
import re
from pathlib import Path
import os
import yaml
import sys
alias_map = {'a': 'cle', 'b': 'motif', 'c': 'chemins', 'd': 'racine', 'e': 'rmt', 'f': 'motifs', 'g': 'cle_pattern_paths', 'h': 'fl'}

def sync_aliases():
    gbl = sys.modules[__name__].__dict__
    for (alias, varname) in alias_map.items():
        if (varname in gbl):
            gbl[alias] = gbl[varname]
cle = 'clé_exemple'
motif = 'motif_exemple'
chemins = ['chemin1', 'chemin2']
racine = Path('/chemin/absolu/vers/racine')
fl = r"""
base_path : "bbb"
lauch_sh : r"*.sh"
launch_py : 
latex_file : writing.tex
pdf_file : writing.pdf
path_vault:   example_vault  
path_writing:   ✍Writing  
path_templates:   👨\u200d💻Automations  
path_table_block_template:   table_block.md  
path_equation_block_template:   equation_block_single.md  
path_equation_blocks:   equation blocks  
path_table_blocks:   table blocks  
path_list_note_paths:   DO_NOT_DELETE__note_paths.txt  
path_BIBTEX:   BIBTEX  
"""
racine = Path(__file__).resolve().parent
rmt = rmt = (lambda racine, motif, dossier1st='d': [str(item) for (dossier, sous_dossiers, fichiers) in os.walk(Path(racine)) 
    for item in ([*((Path(dossier) / racine) for racine in sous_dossiers), *((Path(dossier) / motifs) for motifs in fichiers)] 
    if (dossier1st == 'd') else [*((Path(dossier) / motifs) for motifs in fichiers), *((Path(dossier) / racine) 
        for racine in sous_dossiers)]) if re.search(motif, item.name, re.I)])
parsed_yaml = yaml.safe_load(fl)

motifs = motifs = {cle: ((yaml.safe_load(open('fl.md', encoding='utf-8')) if Path('fl.md').is_file() 
    else {}).get(cle) or val) for (cle, val) in parsed_yaml.items()}

cle_pattern_paths = cle_pattern_paths = {cle: (f'{cle} "{chemins[0]}"' 
    if (chemins := rmt(racine, motif)) 
        else f'{cle} "affich non trouvé"') for (cle, motif) in motifs.items()}

sync_aliases()

print(cle_pattern_paths)
print(cle)
print(cle)
print(motifs)
print(motifs)
for (cle, motif) in motifs.items():
    chemins = rmt(racine, motif)
    print(f'{cle}: {chemins}')
cle = 'nouvelle_clé'
sync_aliases()
print(cle)
