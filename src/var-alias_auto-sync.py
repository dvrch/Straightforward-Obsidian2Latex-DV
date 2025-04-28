Je comprends vos deux demandes : clarifier le mécanisme avec un diagramme Mermaid et modifier la recherche pour qu'elle ne parcoure pas les sous-dossiers. Voici la solution restructurée :

### Version Simplifiée et Corrigée
```python
import re
from pathlib import Path
import os
import yaml

def get_targets(config: dict, root_dir: Path) -> Dict[str, Path]:
    """Trouve le fichier/dossier le plus pertinent pour chaque motif"""
    results = {}
    for key, pattern in config.items():
        if not pattern:  # Ignore les motifs vides
            continue
            
        # Recherche dans le répertoire racine uniquement (pas de os.walk)
        items = [f for f in os.listdir(root_dir) 
                if re.search(pattern, f, re.IGNORECASE)]
        
        if items:  # Prend le premier match trouvé
            results[key] = root_dir / items[0]
    
    return results

# Chargement des configurations
base_dir = Path(__file__).resolve().parent.parent
p1 = yaml.safe_load(fl_content) or {}
p2 = yaml_dict_content_from_file("config.md")  # Votre fichier Markdown

# Fusion : p2 complète p1 sans écraser les valeurs existantes
config = {**{k: v for k, v in p2.items() if v}, **p1}  # Priorité à p1

# Recherche des cibles
root_dir = Path(config.get('base_path', base_dir))  # Racine de recherche
targets = get_targets(config, root_dir)


# ```

# ### Diagramme Mermaid
# ```mermaid
# graph TD
#     A[Fichier FL] -->|yaml.safe_load| B[Dict p1]
#     C[Fichier MD] -->|yaml_dict_content_from_file| D[Dict p2]
#     B --> E{Fusion}
#     D --> E
#     E --> F[Config finale]
#     F --> G[base_path?]
#     G -->|Oui| H[Racine = base_path]
#     G -->|Non| I[Racine = dossier parent]
#     H --> J[Recherche]
#     I --> J
#     J --> K[Scan dossier]
#     K --> L[Filtre par motif]
#     L --> M[Prend 1er match]
#     M --> N[Dict targets]
# ```

# ### Explications :

# 1. **Chemin de base** :
#    - `base_dir` : Chemin par défaut (dossier parent du script)
#    - `base_path` : Optionnel dans la config, sinon utilise `base_dir`

# 2. **Recherche simplifiée** :
#    - Ne parcourt **que le dossier racine** (`os.listdir`)
#    - Pour chaque motif, prend le **premier fichier/dossier correspondant** (`items[0]`)

# 3. **Logique de fusion** :
#    ```python
#    {**{k: v for k, v in p2.items() if v}, **p1}
#    ```
#    - Prend les valeurs non-vides de p2
#    - Les valeurs de p1 ont priorité

# 4. **Sortie** :
#    - Dictionnaire `targets` avec `{clé: chemin_absolu}`

# ### Exemple Résultat :
# Si votre dossier contient :
# ```
# /projet/
#   ├── main.tex
#   ├── run.sh
#   └── docs/
# ```

# Avec la config :
# ```yaml
# latex_file: "\.tex$"
# launch_sh: "\.sh$"
# ```

# Le résultat sera :
# ```python
# {
#     'latex_file': Path('/projet/main.tex'),
#     'launch_sh': Path('/projet/run.sh')
# }
# ```

# Cette version est plus précise et correspond mieux à votre besoin de ne pas explorer les sous-dossiers.