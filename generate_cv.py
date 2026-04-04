import yaml
from jinja2 import Environment, FileSystemLoader
import pdfkit
import sys
import os

def generate_cv():
    # Détermination du dossier racine du projet
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    data_path = os.path.join(current_dir, '_data', 'profile_eng.yml')
    # On initialise le loader sur le dossier des templates
    template_dir = os.path.join(current_dir, '_templates')
    
    # Nom du fichier final à la racine du projet
    output_pdf = os.path.join(current_dir, 'CV_Gregory_LB.pdf')

    print(f"--- Loading data from {data_path} ---")
    with open(data_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # Configuration Jinja2 (comme ton script Academic)
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('engineering.html')
    html_content = template.render(data=data)

    options = {
        'page-size': 'A4',
        'margin-top': '0in',
        'margin-right': '0in',
        'margin-bottom': '0in',
        'margin-left': '0in',
        'encoding': "UTF-8",
        'enable-local-file-access': None,
        'quiet': '' 
    }

    if sys.platform.startswith('win'):
        path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    else:
        # Sur Linux / GitHub Actions
        config = pdfkit.configuration()

    print(f"--- Creating PDF at {output_pdf} ---")
    try:
        # On génère d'abord en string pour vérifier que tout va bien
        pdfkit.from_string(html_content, output_pdf, configuration=config, options=options)
        
        if os.path.exists(output_pdf):
            print(f"✅ PDF successfully created. Size: {os.path.getsize(output_pdf)} bytes")
        else:
            print(f"❌ Critical Error: pdfkit claimed success but {output_pdf} is missing.")
            sys.exit(1)
            
    except Exception as e:
        # Sur GitHub Actions, wkhtmltopdf quitte parfois avec un code 1 même s'il réussit
        if os.path.exists(output_pdf):
            print(f"✅ PDF generated despite technical warning: {e}")
        else:
            print(f"❌ Generation failed: {e}")
            sys.exit(1)

if __name__ == "__main__":
    generate_cv()