import yaml
from jinja2 import Environment, FileSystemLoader

# Read config from YAML file
with open('config.yml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

for conference_key in config:
    file_name = config[conference_key]["output_file_name"]

    # Read talks from YAML file
    with open(f"talks/{file_name}.yml") as file:
        yaml_data = yaml.load(file, Loader=yaml.FullLoader)

    # Load Jinja2 template from file
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('templates/table.html')

    # Render template with YAML data
    output = template.render(talks=yaml_data["talks"], title=config[conference_key]["title"])

    with open(f'html_table/{file_name}.html', 'w') as file:
        file.write(output)