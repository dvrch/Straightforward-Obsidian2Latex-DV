import re


def escape_underscores_in_sections(text):
    """
    Escapes underscores in section-related LaTeX commands such as \\section, \\subsection, etc.
    
    Parameters:
        text (str): A single line of LaTeX code.
    
    Returns:
        str: The line with underscores escaped if it's a section-related command.
    """
    # List of LaTeX sectioning commands to check
    section_commands = ['section', 'subsection', 'subsubsection', 'paragraph', 'subparagraph']
    
    for command in section_commands:
        # Match lines like \section{Some_text_here}
        pattern = rf'(\\{command}\*?\s*\{{)([^}}]*)(\}})'
        match = re.search(pattern, text)
        if match:
            before, content, after = match.groups()
            # Escape underscores in the content part
            escaped_content = content.replace('_', r'\_')
            return f"{before}{escaped_content}{after}"
    
    return text
    

def symbol_replacement(S, SYMBOLS_TO_REPLACE):
    latex_special_chars = ['&', '_', '%', '$', '#', '{', '}', '~', '^', '\\']
    
    S_1 = []
    for s in S:
        s1 = s
        # First handle LaTeX special characters that need escaping
        in_command = False
        in_mathmode = False
        
        # Don't escape if we're inside a LaTeX command or math mode
        new_s = ""
        i = 0
        while i < len(s1):
            if s1[i:i+1] == '$':
                in_mathmode = not in_mathmode
                new_s += s1[i]
            elif s1[i:i+1] == '\\':
                in_command = True
                new_s += s1[i]
            elif s1[i] == '{' and in_command:
                in_command = False
                new_s += s1[i]
            elif s1[i] in latex_special_chars and not in_command and not in_mathmode:
                new_s += '\\' + s1[i]
            else:
                new_s += s1[i]
            i += 1
            
        s1 = new_s
        
        # Then handle symbol replacements from configuration
        for symbol in SYMBOLS_TO_REPLACE:
            obsidian_symbol, latex_replacement, replacement_type = symbol
            # Escape the replacement string for re.sub
            escaped_latex_replacement = re.escape(latex_replacement)
            
            if replacement_type == 0:
                # Simple string replacement
                s1 = re.sub(re.escape(obsidian_symbol), escaped_latex_replacement, s1)
            elif replacement_type == 1:
                # Add space after replacement
                s1 = re.sub(re.escape(obsidian_symbol), escaped_latex_replacement + ' ', s1)
            elif replacement_type == 2:
                # Use regex pattern
                s1 = re.sub(obsidian_symbol, escaped_latex_replacement + ' ', s1)
            
        S_1.append(s1)

    return S_1


def escape_underscores_in_texttt(text):
    """
    Replaces underscores with \\_ inside the brackets of \texttt{}.

    Args:
        text (str): The input LaTeX string.

    Returns:
        str: The modified LaTeX string with escaped underscores inside \texttt{},
             or the original string if no match is found.
    """
    def replace_underscores(match):
        # Escape underscores in the matched text (inside \texttt{})
        return match.group(0).replace('_', r'\_')

    # Regex pattern to find \texttt{...}
    pattern = r'\\texttt\{.*?\}'
    
    # Replace underscores only within \texttt{...} if any matches exist
    replaced_text = re.sub(pattern, replace_underscores, text)
    
    return replaced_text
