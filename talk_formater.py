import yaml
from jinja2 import Environment, FileSystemLoader

# Read config from YAML file
with open('config.yml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# Read talks from YAML file
with open(config["DPG24"]["output_file"]) as file:
    yaml_data = yaml.load(file, Loader=yaml.FullLoader)

# Load Jinja2 template from file
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('templates/table.html')

# Render template with YAML data
output = template.render(talks=yaml_data["talks"], title=config["DPG24"]["title"])

with open('html_table/karlsruhe24.html', 'w') as file:
    file.write(output)