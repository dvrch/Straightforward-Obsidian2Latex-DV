# Excellentes questions ! Voici une fonction compacte et puissante qui :

# - Cherche tous les éléments dont le nom **contient un motif** (pas besoin du nom exact)
# - Permet d’**orienter la recherche** : d’abord dans les dossiers, puis dans les fichiers (ou l’inverse)
# - Utilise la **list comprehension**, le **walrus operator** et **regex**
# - Prend en compte le motif dans l’ordre (gauche → droite) et permet de préciser si tu veux d’abord les dossiers ou les fichiers

# ---


import re
from pathlib import Path
import os

import yaml

# recherche_motif = lambda racine, motif, dossier1st='dossier': [
#     str((Path(dossier) / item).resolve())
#     for dossier, sous_dossiers, fichiers in os.walk(Path(racine))
#     for item in (
#         sous_dossiers + fichiers if dossier1st == 'dossier' else fichiers + sous_dossiers
#     )
#     if re.search(motif, item, re.I)
# ]
# racine = Path(__file__).resolve().parent.parent
# print(recherche_motif(racine, '✍Wri')[0])

recherche_motif = rmt = lambda racine, motif, dossier1st='d': [
    str(item)
    for dossier, sous_dossiers, fichiers in os.walk(Path(racine))
    for item in (
        [*(Path(dossier)/d for d in sous_dossiers), *(Path(dossier)/f for f in fichiers)]
        if dossier1st == 'd'
        else [*(Path(dossier)/f for f in fichiers), *(Path(dossier)/d for d in sous_dossiers)]
    )
    if re.search(motif, item.name, re.I)
]
# Exemple d'utilisation :
racine = Path(__file__).resolve().parent.parent





# motif = r"BIBTEX.*\.bib"  

# # ```python
# import os, re
# from pathlib import Path

# def recherche_motif(racine, motif, dossier1st='dossier'):
#     """
#     racine : dossier de départ (Path ou str)
#     motif : motif regex (str)
#     dossier1st : 'dossier' ou 'fichier' (précise où chercher en priorité)
#     """
#     regex = re.compile(motif, re.I)
#     matches = []
#     for dossier, sous_dossiers, fichiers in os.walk(racine):
#         # Dossiers d'abord
#         if dossier1st == 'dossier':
#             matches += [os.path.join(dossier, d) for d in sous_dossiers if regex.search(d)]
#             matches += [os.path.join(dossier, f) for f in fichiers if regex.search(f)]
#         # Fichiers d'abord
#         else:
#             matches += [os.path.join(dossier, f) for f in fichiers if regex.search(f)]
#             matches += [os.path.join(dossier, d) for d in sous_dossiers if regex.search(d)]
#     return matches

    # Cherche tout ce qui ressemble à 'BIBTEX.bib' (insensible à la casse)

fl = """ 
base_path : "bbb"
lauch_sh : r"*.sh"
launch_py : 
latex_file : writing.tex
pdf_file : writing.pdf
path_vault:   example_vault  
path_writing:   ✍Writing  
path_templates:   👨‍💻Automations  
path_table_block_template:   table_block.md  
path_equation_block_template:   equation_block_single.md  
path_equation_blocks:   equation blocks  
path_table_blocks:   table blocks  
path_list_note_paths:   DO_NOT_DELETE__note_paths.txt  
path_BIBTEX:   BIBTEX  
""" # les valeurs prdefaut 

motifs =f = {cle: (yaml.safe_load(open("fl.md", encoding="utf-8")) 
            if Path("fl.md").is_file() else {}).get(cle) 
                or val for cle, val in yaml.safe_load(fl).items()}


cle_pattern_paths = clpp = {
    cle: f"{cle} {(f'\"{chemins[0]}\"' 
                       if (chemins := rmt(racine, motif)) 
                       else '\"affich non trouvé\"')}"
    for cle, motif in motifs.items()
}

f"{clpp[key]} = clpp[{clpp[key]}]"  for key in motifs.keys() 

[f"{clpp[cle]} = {}" for clpp, motif in motifs.items() if motif]

# resultats = [f"{cle:<18} {(f'\"{chemins[0]}\"' if (chemins := rmt(racine, motif)) 
#                   else '\"affich non trouvé\"'):<60}"
#     for cle, motif in motifs.items()]

# resultats2 = [
#     *[
#         f"{i+1:<4} {cle:<12} {motif:<25} " f"{f'\"{chemins[0]}\"' 
#                                               if (chemins := rmt(racine, motif)) 
#                                               else '\"affich non trouvé\"':<40}"
#         for i, (cle, motif) in enumerate(motifs.items())
#     ],
#     '-' * 85,
#     f"{'N°':<4} {'Clé':<12} {'Motif recherché':<25} {'Chemin trouvé':<40}",
# ]

# resultats[N:=6-1].split(maxsplit=3)[3]  # -1 car commence a 0 zero | 3e element apres 3split, (les)
# # -------------------------------

# ```

# ---

# ### Explications

# - **motif** : regex, donc `"BIBTEX.*\.bib"` trouve tous les fichiers/dossiers contenant "BIBTEX" et finissant par ".bib".
# - **dossier1st** : `'dossier'` pour prioriser les dossiers, `'fichier'` pour prioriser les fichiers.
# - **matches** : liste de tous les chemins trouvés, dans l’ordre demandé.

# ---

# ### Pour spécifier la direction dans le motif

# - Si tu veux "BIBTEX" en début de nom, mets : `r"^BIBTEX.*\.bib"`
# - Si tu veux "BIBTEX" n’importe où, mets : `r"BIBTEX.*\.bib"`
# - Si tu veux d’abord les dossiers, puis les fichiers, utilise `dossier1st='dossier'` (défaut)
# - Inversement, pour les fichiers d’abord, utilise `dossier1st='fichier'`

# ---

# **Ce code est compact, flexible, puissant et réutilisable !**  
# N’hésite pas à demander des variantes ou précisions !

# ---
# Réponse de Perplexity: pplx.ai/share


# --------------------------
# import os

# racine = Path(__file__).resolve().parent.parent
# nom_recherche = 'BIBTEX.bib'  # Remplace par le nom exact

# for dossier, sous_dossiers, fichiers in os.walk(racine):
#     if nom_recherche in fichiers or nom_recherche in sous_dossiers:
#         chemin = os.path.join(dossier, nom_recherche)
#         print(chemin)
#         break  # retire ce break si tu veux trouver tous les éléments du même nom





# ligne = resultats[N:=4-1]  # +1 car il y a l’en-tête et la séparation
# chemin = ligne.split(maxsplit=3)[3]
# print(chemin)


# 