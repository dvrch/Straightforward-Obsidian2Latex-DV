import os
from pathlib import Path
import re
def get_parameters(version = 'default'):
    
    '''
    Get the parameters for the file conversion
    '''
    
    # Helper functions
    def conv_dict(D):
        for key, value in D.items():
            if value == '🟢':
                D[key] = True
            elif value == '🔴':
                D[key] = False
            elif isinstance(value, dict):
                D[key] = conv_dict(value)
        return D

    def python_format_path(path, to_python = False):
        
        if not to_python:
            return path.replace('\\\\', '\\')
        else:
            return path.replace('\\', '\\\\')

        
    
    # Global constants
    ID__TABLES__alignment__center = 0
    ID__TABLES__alignment__right  = 1
    ID__TABLES__alignment__middle = 2


    ID__TABLES__PACKAGE__longtblr   = 0
    ID__TABLES__PACKAGE__tabularx   = 1
    ID__TABLES__PACKAGE__long_table = 2

    ID__CNV__TABLE_STARTED      = 0
    ID__CNV__TABLE_ENDED        = 1
    ID__CNV__IDENTICAL          = 2

    ID__STYLE__BOLD             = 0
    ID__STYLE__HIGHLIGHTER      = 1
    ID__STYLE__ITALIC           = 2
    ID__STYLE__STRIKEOUT        = 3

    ID__DOCUMENT_CLASS__ARTICLE = 'article'
    ID__DOCUMENT_CLASS__EXTARTICLE = 'extarticle'
    ID__DOCUMENT_CLASS__CONFERENCE__IFAC = 'ifacconf'

    # ⚠ does not work for longtblr!
    CMD__TABLE__TABULARX__CENTERING = '\\newcolumntype{Y}{>{\\centering\\arraybackslash}X}'
    #

    #  %%
    # USER PARAMETERS
    import yaml
    from pathlib import Path
    import os

    path_personalisation =  Path(os.getcwd(), "example_vault", "✍Writing", "personalisation des paths.yaml")
    # Charger les configurations depuis un fichier YAML externe
    with open(path_personalisation, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    # Fonction utilitaire pour gérer les chemins vides ou invalides
    def get_path_or_default(config_content, key, default_path):
        path_str = config_content.get(key, '')
        if path_str and Path(path_str).exists():
            print(f"✅ personalisation de {key}: {path_str}")  # Ajout de cette ligne
            return Path(path_str)
        else:
            return default_path
        #  %%

    GP_D = get_path_or_default
    work_dir_tex = GP_D(config, 'work_dir_tex', Path(os.getcwd())) # work_dir_tex =Path(__file__).parent.parent  >>> a patir du fichier
    path_vault = GP_D(config, 'path_vault', work_dir_tex/'example_vault')
    path_writing = GP_D(config, 'path_writing', path_vault/'✍Writing')
    path_templates = GP_D(config, 'path_templates', path_vault/'👨‍💻Automations')
    path_table_block_template = GP_D(config, 'path_table_block_template', path_templates/'table_block.md')
    path_equation_block_template = GP_D(config, 'path_equation_block_template', path_vault/'👨‍💻Automations'/'equation_block_single.md')  # corrected line
    path_table_blocks = GP_D(config, 'path_table_blocks', path_writing/'table blocks')
    path_equation_blocks = GP_D(config, 'path_equation_blocks', path_writing/'equation blocks')
    path_list_note_paths = GP_D(config, 'path_list_note_paths', path_vault/'DO_NOT_DELETE__note_paths.txt')
    path_BIBTEX_bib = GP_D(config, 'path_BIBTEX','BIBTEX.bib') # fichier>>>+ tard, diviser en folder/file
    # path_BIBTEX_path = GP_D(config, 'path_BIBTEX_path', path_writing/'BIBTEX.bib') # a voir

    # Ajout des nouveaux chemins
    convert_file_md = GP_D(config, 'convert_file_md', path_vault/'✍Writing'/'👨‍💻convert_to_latex.md')
    path_compile_script = GP_D(config, 'path_compile_script', path_vault/'✍Writing'/'compile_and_open.sh')
    path_converter = GP_D(config, 'path_converter', work_dir_tex/'converter.py')
    path_example_pdf = GP_D(config, 'path_example_pdf', path_writing/'example_writing.pdf')
    path_example_tex = GP_D(config, 'path_example_tex', path_writing/'example_writing.tex')

    file_name4sh = GP_D(config, 'file_name4sh', 'example_writing')

    path_custom_latex_commands = GP_D(config, 'path_custom_latex_commands', path_vault/'✍Writing'/'custom_latex_functions.tex')


    # Intégrer directemoent ici les scripts bash et python pour éviter la duplication des chemins et variables

    def update_paths():
                # Mise à jour du fichier convert_to_latex.md

        if convert_file_md.exists():
            with open(convert_file_md, 'r', encoding='utf-8') as f:
                content = f.read()

            # Pour code_run::
            content = re.sub(
                r'(\[1\. 👨‍💻🖱convert\])\(<file:[^)]+>\)',
                rf'\1(<file:///{path_converter.as_posix()}>)',
                content
            )
            content = re.sub(
                r'(\[2\. 👨‍💻compile to \.pdf\])\(<file:[^)]+>\)',
                rf'\1(<file:///{path_compile_script.as_posix()}>)',
                content
            )

            # Pour files::
            content = re.sub(
                r'(\[📁tex file\])\(<file:[^)]+>\)',
                rf'\1(<file:///{path_example_tex.as_posix()}>)',
                content
            )
            content = re.sub(
                r'(\[📁\.pdf file\])\(<file:[^)]+>\)',
                rf'\1(<file:///{path_example_pdf.as_posix()}>)',
                content
            )

            with open(convert_file_md, 'w', encoding='utf-8') as f:
                f.write(content)
                print(f"✅ Mise à jour de {convert_file_md.name}")
        else : # write the file whith r'''

            with open(convert_file_md, 'w', encoding='utf-8') as f:
                f.write(rf'''
# %%
# ℹ Instructions
# - in the "convert_note" field, link the note you wish to convert (only one note)
# - in the "code_run" field, set the paths of the python script and the .bat file accordingly
# - in the "files" field, set the paths accordingly

## Things that can create errors
### Package irregularities

# ![[table__block_latex_packages_that_should_not_be_combined#table]]


# # Previous jobs
# Can save previously converted notes here
# %%

# convert_note:: [[example_writing]]
# --

# ---

# code_run:: [1. 👨‍💻🖱convert](<file:///{path_converter}# >) , [2. 👨‍💻compile to .pdf](<file:///{path_compile_script}>)
# --


# ---


# files::  [📁tex file](<file:///{path_example_tex}>), [📁.pdf file](<file:///{path_example_pdf}>)
# -- 

# ---

''')
                print(f"✅ Création de {convert_file_md.name}")

            

        # Mise à jour du fichier compile_and_open.sh
        if path_compile_script.exists():
            with open(path_compile_script, 'r', encoding='utf-8') as f:
                content = f.readlines()
                
            # Mettre à jour les chemins dans le fichier bash
            for i, line in enumerate(content):
                if line.startswith('BASE_PATH='):
                    content[i] = f'BASE_PATH="{str(path_writing)}"\n'
                elif line.startswith('FILE_NAME='):
                    content[i] = f'FILE_NAME="{str(file_name4sh)}"\n'
                    
            with open(path_compile_script, 'w', encoding='utf-8', newline='\n') as f:
                f.writelines(content)
            print(f"✅ Mise à jour de {path_compile_script.name}")
        
        else:
            with open(path_compile_script, 'w', encoding='utf-8') as f:
                f.write(rf'''
#!/bin/bash
# This file compiles the latex file to .pdf

# Set base path and file name
BASE_PATH="{str(path_writing)}"
FILE_NAME="{str(file_name4sh)}"
TEXFILE="$BASE_PATH/$FILE_NAME.tex"
PDFFILE="$BASE_PATH/$FILE_NAME.pdf"

# Print paths for debugging
echo "TEXFILE: $TEXFILE"
echo "PDFFILE: $PDFFILE"

# Compile the LaTeX file
pdflatex -interaction=nonstopmode -shell-escape "$TEXFILE"
if [ $? -ne 0 ]; then
    echo "pdflatex compilation failed."
    exit 1
fi

# Open the resulting PDF file
# Use 'start' on Windows (Git Bash) and 'xdg-open' on Linux/macOS
if [[ "$OSTYPE" == "msys" ]]; then
  start "$PDFFILE"
else
  xdg-open "$PDFFILE"
fi
                        
''')

    # Appeler la fonction à l'import si besoin
    update_paths()
    # %%

    
    # work_dir_tex =Path(os.getcwd())  # avec 🧡 et en guise de remerciement
    # # work_dir_tex =Path(__file__).parent.parent

    # path_vault          =  Path(work_dir_tex/'example_vault')
    # path_writing        = Path(path_vault/'✍Writing')
    # path_templates        = Path(path_vault/'👨‍💻Automations')
    # path_table_block_template = Path(path_templates/'table_block.md')
    # path_equation_block_template = Path(path_templates/'equation_block_single.md')  # corrected line
    # path_table_blocks   = Path(path_writing/'table blocks')

    # path_equation_blocks = Path(path_writing/'equation blocks')
    # path_list_note_paths = Path(path_vault/'DO_NOT_DELETE__note_paths.txt')
    # path_BIBTEX_bib          = Path(path_writing/'BIBTEX')
    
    if not os.path.exists(path_list_note_paths):
        with open(path_list_note_paths, 'w', encoding='utf-8') as file:
            file.write('')
    
    for path in [path_writing, path_equation_blocks, path_table_blocks, path_templates]:
        if not os.path.exists(path):
            os.makedirs(path)
            
    if not os.path.exists(path_table_block_template):
        with open(path_table_block_template, 'w', encoding='utf-8') as file:
            file.write(table_block_text())
        
    if not os.path.exists(path_equation_block_template):
        with open(path_equation_block_template, 'w', encoding='utf-8') as file:
            file.write(equation_block_text())
            
    path_plugins = Path(path_vault / '.obsidian' / 'plugins')
    path_quick_add = Path(path_plugins / 'quickadd')

    # if not os.path.exists(path_quick_add):
    #     shutil.copytree('\\'.join(os.path.abspath(__file__).split('\\')[0:-2]) + '\\obsidian\\.obsidian\\plugins\\quickadd', path_plugins)
    # else:
    #     raise Exception('Not implemented yet.')
                
    hyperlinkSetup = r"""
    \hypersetup{
    colorlinks   = true,    % Colours links instead of ugly boxes
    urlcolor     = blue,    % Colour for external hyperlinks
    linkcolor    = blue,    % Colour of internal links
    citecolor    = blue      % Colour of citations
    }
    """
    
    
    # apply parameter changes based on specific notes
        
    V__document_class = {'class': ID__DOCUMENT_CLASS__EXTARTICLE, 'fontsize': ''}
    V__author = 'DJONTSO Victorien'  # Marios Gkionis' 
        
    if version =='[[👆👆RL--writing--1]]':
        
        V__document_class = {'class': ID__DOCUMENT_CLASS__EXTARTICLE, 'fontsize': '12pt'}
        V__author = ''
        
    elif version =='[[✍⌛writing--FaultDiag--Drillstring--MAIN]]':
        
        V__document_class = {'class': ID__DOCUMENT_CLASS__CONFERENCE__IFAC, 'fontsize': ''}
        V__author = ''
         
    # elif version =='[✍⌛writing--THESIS--high-level-structure]]':
        
    #     #\documentclass[a4paper, 12pt, openany]{book}

    # %%
    PARS = conv_dict({
        '⚙': # SETTINGS 
            {'SEARCH_IN_FILE': {'condition':'🔴', 'text_to_seach': 'w_{E_{2}}','replace_with': '\\beta_{2}'},
             'document_class': V__document_class,
            'TABLES':{
                                'package': ID__TABLES__PACKAGE__tabularx,
                    'hlines-to-all-rows': '🟢',
                    'any-hlines-at-all': '🟢',
                            'alignment':  [ID__TABLES__alignment__center,
                                            ID__TABLES__alignment__middle],
                            'rel-width': 1.2,
                    },
            'margin': '0.9in',
            'use_date': '🔴',
            'EXCEPTIONS': 
                        {'raise_exception__when__embedded_reference_not_found': '🔴'},
            'INTERNAL_LINKS': 
                            {'add_section_number_after_referencing': '🟢'  # if True, then we have "\hyperref[sBootstrapping-and-the-iterative-logic-in-estimation]{here}: \autoref{sBootstrapping-and-the-iterative-logic-in-estimation}". 
                            },        
            'EMBEDDED REFERENCES':  
                            {'convert_non_embedded_references': '🟢',  # if True, then references such as "[[another note]]" will be changed to "another note". If FAlse, they will remain as is
                            'treat_equation_blocks_separately': '🟢', # if True, then the equation blocks are treated separately, in order to increase speed
                                             'treat_citations': '🟢',
                                     'adapt_section_hierarchy': '🟢', # if True, then whenever there are sections in an embedded reference, their hierarchy will change, based on whether the embedded note was already in sections (so we don't break the hierarchy)
                    'write_obsidian_ref_name_on_latex_comment': '🟢'}, 
            'figures': 
                            {'reduce spacing between figures': '🔴',
                                      'put_figure_below_text': '🟢',
                                               'include_path': '🟢', # not including the path works only if all the figures are in the same folder (appropriate for Overleaf projects)
                        'use_overleaf_all_in_the_same_folder': '🔴'}, 
                                                        
            'paragraph':{
                        'indent_length_of_first_line': 0,    # 0 if no indent is desired. Recommended 20 for usual indent
                        'if_text_before_first_section___place_before_table_of_contents': '🔴',
                        'insert_new_line_symbol':                                        '---',
                        'add_table_of_contents':                                        '🔴',
                        'add_new_page_before_bibliography':                             '🟢',
                        'allowdisplaybreaks':                                           '🔴',
            }, 
            'author': V__author,
            'title': '',
            'hyperlink_setup': hyperlinkSetup,
            'code_blocks': {
                            'admonition':  [
                                            ['default', ['white', 'black']],
                                            ['warning', ['red', 'white']],
                                            ['quote',   ['gray', 'black']],
                                            ['todo',    ['yellow', 'red']]
                                        ]
                },
            'formatting_rules':{
                        'non_embedded_references': { # find list of colors here: https://www.overleaf.com/learn/latex/Using_colors_in_LaTeX
                                                    'notes_with_tags': [ # add tag, color ("\textcolor{}{}" function)
                                                                        ["#Latex/Formatting/method",         "teal"],
                                                                        ["#Latex/Formatting/characteristic", "gray"],
                                                                        ["#Latex/Formatting/task",           "red"],
                                                                        ['#Latex/Formatting/math-term',      "brown"]
                                                                        ]}
            }},
        '📁': # Paths 
            {
                    'command_note': Path(path_vault/'✍Writing'/'👨‍💻convert_to_latex.md'),
                           'vault': path_vault,
                 'equation_blocks': path_equation_blocks,
                'list_paths_notes': path_list_note_paths, # saves time from searching of the note's path (the DO_NOT_DELETE
                     'bash_script': path_compile_script,
                'bibtex_file_name': path_BIBTEX_bib, # your bibtex file name
                     'bibtex_path': path_BIBTEX_bib,
            'custom_latex_commands': path_custom_latex_commands,
                },
        'par':
            {
                'tabular-package':
                                {
                                        'names': ['longtblr', 'tabularx'],
                                    'before-lines': ['{colspec}']
                                },
                'packages-to-load':[ # preamble packages, #exclude for doc_class  # comment (placed inside the latex file, next to the package loading)      
                                    ['hyperref',    None,                                    ''],
                                    ['graphicx',    None,                                    ''],
                                    ['subcaption',  None,                                    'for subfigures'],
                                    ['amssymb',     None,                                    'need more symbols'],
                                    ['titlesec',    ID__DOCUMENT_CLASS__CONFERENCE__IFAC,    "so that we can add more subsections (using 'paragraph')"],
                                    ['xcolor, soul',None,                                   'for the highlighter'],
                                    ['amsmath',     None,                                    ''],
                                    ['amsfonts',    None,                                    ''],
                                    ['cancel',      None,                                    ''],
                                    ['minted',      None,                                    ''],
                                    ['apacite',     None,                                    'apa citation style'],
                                    ['caption',     None,                                    'to set smaller vertical spacing between two figures'],
                                    ['cleveref',    None,                                    'for clever references'],
                                    ['tcolorbox',   None,                                    ''],
                                    ['float',       None,                                    'to make the figures stay between the text at which they are defined'],
                                    ['pdfpages',    None,                                     ''],
                                    ['totcount',    None,                                     ''],
                                    ['lipsum',      None,                                     ''],
                                    ['ragged2e',    None,                                     'can wrap text for tables in the tabularx environment'],
                                    ['natbib',      None,                                     "Such that we avoid the error (`Illegal parameter number in definition of \\reserved@a`) of not being able to add citations in captions"],
                                    ['pdfcomment',  None,                                     'for popup comments in the .pdf'],
                                    ['booktabs',    None,                                      'so that the toprule command works'],
                                    ['soul',        None,                                      'to strikeout text using \\st{}'],
									['twemojis',	None,										'for twemojis'],			
                                    ['rotating',    None,                                       'for rotating text on tables']						
                                    ],
            'symbols-to-replace': [  # Obsidian symbol, latex symbol, type de remplacement (1 ou 2)
    ['✔',              r'\checkmark',                   1],
    ['🟢',             '$\\blacklozenge$',             2],
    ['🔴',             r'\\maltese',                     2],
    ['➕',             r'\twemoji{plus}',              1],
    ['🔗',             'LINK',                          1],
    [r'implies',      r'\Rightarrow',                1],
    ['❓❓',            '?',                             1],
    ['❓',             '?',                             1],
    ['❌',             'NO',                            1],
    ['🤔',            r'\twemoji{thinking-face}',     1],
    ['⚠',              r'\twemoji{warning}',    1],
    ['📚',             r'\twemoji{books}',      1],
    ['📜',            r'\twemoji{page with curl}',                      1],
    ['⌛',               r'\twemoji{hourglass}',                     1],
    ['🔭',              r'\twemoji{telescope}',                     1],
    ['👆',              r'\twemoji{index pointing up}',                      1],
    ['💭',              r'\twemoji{thought balloon}',                      1],
    ['🔧',              r'\twemoji{screwdriver}', 1],
           									['⛏',				 r'\twemoji{pick}',        1],
											['⏳',				 r'\twemoji{hourglass}',   1],
                                            ['🧪',                  r'\twemoji{test tube}',           1],
                                            ['⭐',                  r'\twemoji{star}',           1],
                                            ['💡',                  r'\twemoji{light bulb}',           1],
											['📅',                  r'\twemoji{date}',           1],
                                            ['📍',                r'\twemoji{round pushpin}',           1],
                                            ['📜',                  r'\twemoji{scroll}',          1] ,
                                            ]
            },
            #                                        ['\\text',          '\\textnormal',          1],

        'EQUATIONS':
                {'convert_non_numbered_to_numbered': '🟢'} # If True, all equations are numbered
    })
       

    return PARS



def equation_block_text():
    text = """
# %%expr%%
    """
    return text

def table_block_text():
    text = """
%%
caption:: 
widths:: 
package:: #Latex/Table/package/  
use_hlines:: 
use_vlines:: 

If the table is a dataview table:
datav__file_column_name:: 

%%
# %%table%%
📣*`=this.caption`*
    """
    
    return text
    
    
def quick_add_table_block_text():
    templatePath = r"👨‍💻Automations/table_block"
    destinationPath = r"✍Writing/table_blocks"
    
    text = f"""
    {{
      "id": "d8dcaf45-4e62-4860-ba69-42671bac884c",
      "name": "table_block",
      "type": "Template",
      "command": true,
      "templatePath": "{templatePath}",   # ✅ Add quotes
      "fileNameFormat": {{
        "enabled": true,
        "format": "table__block_"
      }},
      "folder": {{
        "enabled": true,
        "folders": [
          "{destinationPath}"   # ✅ Add quotes
        ],
        "chooseWhenCreatingNote": false,
        "createInSameFolderAsActiveFile": false,
        "chooseFromSubfolders": false
      }},
      "appendLink": true,
      "openFileInNewTab": {{
        "enabled": true,
        "direction": "vertical",
        "focus": true
      }},
      "openFile": true,
      "openFileInMode": "default",
      "fileExistsMode": "Increment the file name",
      "setFileExistsBehavior": true
    }}
    """  

    return text

if __name__ == '__main__':
    # Code de test pour le débogage
    import logging
    import re
    logging.basicConfig(level=logging.DEBUG)
    
    # Test avec différentes versions
    versions = ['default', '[[👆👆RL--writing--1]]']
    
    for version in versions:
        logging.debug(f"Testing version: {version}")
        params = get_parameters(version)
        logging.debug(f"Document class: {params['⚙']['document_class']}")
        logging.debug(f"Paths created: {list(params['📁'].keys())}")
