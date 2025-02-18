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
    template_en = env.get_template('templates/table_en.html')
    template_de = env.get_template('templates/table_de.html')

    # Render template with YAML data
    output_en = template_en.render(talks=yaml_data["talks"], title=config[conference_key]["title_en"])
    output_de = template_de.render(talks=yaml_data["talks"], title=config[conference_key]["title_de"])

    with open(f'html_table/{file_name}_en.html', 'w') as file:
        file.write(output_en)

    with open(f'html_table/{file_name}_de.html', 'w') as file:
        file.write(output_de)    
