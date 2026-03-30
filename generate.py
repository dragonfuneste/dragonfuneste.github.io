import yaml
from jinja2 import Environment, FileSystemLoader

# Configuration pour LaTeX (délimiteurs modifiés pour éviter les conflits avec LaTeX)
latex_env = Environment(
    block_start_string='((%', block_end_string='%))',
    variable_start_string='[[', variable_end_string=']]',
    loader=FileSystemLoader('templates')
)

# Configuration pour HTML (délimiteurs standards)
html_env = Environment(loader=FileSystemLoader('templates'))

def main():
    with open('_data/profileV2.yml', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # 1. Générer le fichier .tex pour le CV Académique
    template_tex = latex_env.get_template('academic.tex')
    with open('cv_academic.tex', 'w', encoding='utf-8') as f:
        f.write(template_tex.render(data))

    # 2. Générer le fichier .html pour le CV Ingénierie
    template_html = html_env.get_template('engineering.html')
    with open('cv_engineering.html', 'w', encoding='utf-8') as f:
        f.write(template_html.render(data))

if __name__ == "__main__":
    main()