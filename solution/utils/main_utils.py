import yaml
import sys
import json

def read_yaml(file_path):
    try:
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
            return config
    except FileNotFoundError:
        print(f"Error: The file at path {file_path} was not found.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error: Failed to parse YAML file at path {file_path}. Error: {e}")
        sys.exit(1)
        
def write_yaml(file_path, json_content):
    try:
        # Parse the JSON content
        data = json.loads(json_content)
        
        # Write the data to a YAML file
        with open(file_path, 'w') as yaml_file:
            yaml.dump(data, yaml_file, default_flow_style=False)
            
        print(f"Data successfully written to {file_path}")
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON content. {e}")
    except Exception as e:
        print(f"Error: An unexpected error occurred. {e}")