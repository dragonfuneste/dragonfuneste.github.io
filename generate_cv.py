import yaml
from jinja2 import Environment, FileSystemLoader
import pdfkit
import sys
import os

def generate_cv():
    # Base directory of the project
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Correcting the paths based on your 'tree' output
    data_path = os.path.join(current_dir, '_data', 'profile_eng.yml')
    # Changed from '_templates' to 'templates'
    template_dir = os.path.join(current_dir, 'templates')
    
    output_pdf = os.path.join(current_dir, 'CV_Gregory_LB.pdf')

    print(f"--- Loading data from {data_path} ---")
    if not os.path.exists(data_path):
        print(f"❌ Error: Data file not found at {data_path}")
        sys.exit(1)

    with open(data_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # Initialize Jinja2 with the 'templates' directory
    env = Environment(loader=FileSystemLoader(template_dir))
    
    try:
        template = env.get_template('engineering.html')
    except Exception as e:
        print(f"❌ Error: Could not find engineering.html in {template_dir}")
        print(f"Exception: {e}")
        sys.exit(1)

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

    # Configuration for wkhtmltopdf
    if sys.platform.startswith('win'):
        path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    else:
        config = pdfkit.configuration()

    print(f"--- Creating PDF at {output_pdf} ---")
    try:
        pdfkit.from_string(html_content, output_pdf, configuration=config, options=options)
        if os.path.exists(output_pdf):
            print(f"✅ PDF successfully created. Size: {os.path.getsize(output_pdf)} bytes")
    except Exception as e:
        if os.path.exists(output_pdf):
            print(f"✅ PDF generated despite technical warning: {e}")
        else:
            print(f"❌ Generation failed: {e}")
            sys.exit(1)

if __name__ == "__main__":
    generate_cv()