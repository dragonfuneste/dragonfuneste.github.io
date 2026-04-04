import yaml
from jinja2 import Environment, FileSystemLoader

# Configuration pour LaTeX
latex_env = Environment(
    block_start_string='((%', 
    block_end_string='%))',
    variable_start_string='[[', 
    variable_end_string=']]',
    loader=FileSystemLoader('templates')
)

def main():
    # Lecture du YAML
    with open('_data/profile_eng.yml', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # Génération du fichier .tex
    template_tex = latex_env.get_template('academic.tex')
    with open('cv_academic_eng.tex', 'w', encoding='utf-8') as f:
        f.write(template_tex.render(data))
    
    print("cv_academic_eng.tex a été généré avec succès.")

    # Lecture du YAML
    with open('_data/profile_fr.yml', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # Génération du fichier .tex
    template_tex = latex_env.get_template('academic.tex')
    with open('cv_academic_fr.tex', 'w', encoding='utf-8') as f:
        f.write(template_tex.render(data))
    
    print("cv_academic_fr.tex a été généré avec succès.")
if __name__ == "__main__":
    main()