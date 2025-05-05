import re

def symbol_replacement(S, SYMBOLS_TO_REPLACE):
    S_1 = []
    for s in S:
        s1 = s
        for symbol in SYMBOLS_TO_REPLACE:
            try:
                s2 = symbol[2]
                if s2 == 0:
                    # Utiliser replace() pour les remplacements simples
                    s1 = s1.replace(symbol[0], symbol[1])
                elif s2 == 1:
                    s1 = s1.replace(symbol[0], symbol[1] + ' ')
                elif s2 == 2:
                    # Pour les regex, traiter différemment les emojis et caractères spéciaux
                    if any(ord(c) > 127 for c in symbol[0]):  # Détecte les emojis
                        s1 = s1.replace(symbol[0], symbol[1] + ' ')
                    else:
                        pattern = re.escape(symbol[0])
                        s1 = re.sub(pattern, symbol[1] + ' ', s1)
                else:
                    raise Exception("Nothing coded for this case!")
            except re.error as e:
                print(f"Warning: Invalid regex pattern '{symbol[0]}': {e}")
                continue
            except Exception as e:
                print(f"Warning: Error processing pattern '{symbol[0]}': {e}")
                continue
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
