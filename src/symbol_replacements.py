import re

def clean_latex_content(text):
    """Nettoie et corrige les balises LaTeX problématiques"""
    # Nettoyer les espaces autour des commandes
    text = re.sub(r'\s*(\\[a-zA-Z]+)', r'\1', text)
    
    # Corriger les erreurs courantes
    text = text.replace(r'\begin{PCKG_NAME}', r'\begin{tabular}')  # Correction tabular
    text = text.replace('\\\\end{tabular}', r'\end{tabular}')  # Double backslash
    text = text.replace('#', r'\#')  # Échapper les #
    text = text.replace(r'\n\n\n', r'\n\n')  # Trop de sauts de ligne
    
    # Corriger les espaces dans les équations
    text = re.sub(r'\$\s+\\begin', r'$\\begin', text)
    text = re.sub(r'\\end\s+\$', r'\\end$', text)
    
    # Supprimer les balises Cref inutiles
    text = re.sub(r'!\\Cref\{([a-zA-Z0-9:]+)\\\\#([a-zA-Z0-9]+)\}', r'\\Cref{\1}', text)
    
    return text

def symbol_replacement(S, SYMBOLS_TO_REPLACE):
    S_1 = []
    for s in S:
        s1 = s
        for symbol in SYMBOLS_TO_REPLACE:
            try:
                s2 = symbol[2]
                if s2 == 0:
                    s1 = s1.replace(symbol[0], symbol[1])
                elif s2 == 1:
                    # Éviter les espaces en trop
                    s1 = s1.replace(symbol[0], symbol[1].strip() + ' ')
                elif s2 == 2:
                    pattern = re.escape(symbol[0])
                    # Nettoyer les espaces autour du remplacement
                    s1 = re.sub(pattern, symbol[1].strip() + ' ', s1)
                else:
                    raise Exception("Nothing coded for this case!")
            except re.error as e:
                print(f"Warning: Invalid regex pattern '{symbol[0]}': {e}")
                continue
        # Nettoyer le résultat final
        s1 = clean_latex_content(s1) 
        S_1.append(s1)
    return S_1


def escape_underscores_in_texttt(text):
    r"""
    Remplace les underscores par \_ dans les accolades de \texttt{}.
    Utilise une raw string pour gérer les backslashes.

    Args:
        text (str): Le texte LaTeX d'entrée.

    Returns:
        str: Le texte LaTeX modifié avec les underscores échappés dans \texttt{},
             ou le texte original si aucune correspondance n'est trouvée.
    """
    def replace_underscores(match):
        # Échappe les underscores dans le texte correspondant
        content = match.group(0)
        if '_' in content:
            prefix = content[:content.find('{')+1]
            suffix = content[content.rfind('}'):]
            middle = content[content.find('{')+1:content.rfind('}')]
            escaped = middle.replace('_', r'\_')
            return prefix + escaped + suffix
        return content

    pattern = r'\\texttt\{[^}]*\}'
    
    return re.sub(pattern, replace_underscores, text)
